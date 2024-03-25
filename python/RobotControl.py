import socket  # for socket
from enum import Enum
from socket import socket as Socket
from time import sleep
from typing import Callable
from socket import gethostbyname, gethostname

import select

from RobotSocketMessages import CommandFinished, VariableObject, VariableTypes
from SocketMessages import CommandMessage
from ToolBox import escape_string, time_print
from URIFY import URIFY_return_string, SOCKET_NAME
from undo.History import History
from undo.State import State

POLYSCOPE_IP = "polyscope"
_DASHBOARD_PORT = 29999
_PRIMARY_PORT = 30001
_SECONDARY_PORT = 30002
_INTERPRETER_PORT = 30020


def create_get_socket_function() -> Callable[[str, int], Socket]:
    inner_socket_bank: dict[tuple[str, int], Socket] = dict()

    def inner_get_socket(ip: str, port: int) -> Socket | None:
        if (ip, port) in inner_socket_bank:
            return inner_socket_bank[(ip, port)]
        try:
            my_socket: Socket = Socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"Socket successfully created for {ip}:{port}")
        except socket.error as err:
            print(f"socket creation failed with error {err}")
            return

        try:
            my_socket.connect((ip, port))
            print(f"Socket connected to {ip}:{port}")
        except ConnectionRefusedError:
            print(f"Connection to {ip}:{port} refused - retrying in 1 second")
            sleep(1)
            return get_socket(ip, port)

        my_socket.setblocking(False)
        inner_socket_bank[(ip, port)] = my_socket
        return my_socket

    return inner_get_socket


get_socket = create_get_socket_function()

_interpreter_open = False


def get_dashboard_socket():
    return get_socket(POLYSCOPE_IP, _DASHBOARD_PORT)


def get_secondary_socket():
    return get_socket(POLYSCOPE_IP, _SECONDARY_PORT)


def start_interpreter_mode():
    secondary_socket = get_secondary_socket()
    clear_queue_on_enter = "clearQueueOnEnter = True"
    clear_on_end = "clearOnEnd = True"
    send_command(f"interpreter_mode({clear_queue_on_enter}, {clear_on_end})", secondary_socket)
    print("Interpreter mode command sent")


def restart_interpreter_mode():
    start_interpreter_mode()
    # Todo: For some reason the robot needs a sleep here, otherwise open_socket does not work.
    #  I thought the parameters on interpreter_mode would fix this.
    sleep(1)
    apply_variables_to_robot(list_of_variables)
    open_socket()


def clear_interpreter_mode():
    send_command("clear_interpreter()", get_interpreter_socket())
    print("Clear command sent")


def power_on_robot():
    dashboard_socket = get_dashboard_socket()
    send_command("power on", dashboard_socket)


def brake_release_on_robot():
    dashboard_socket = get_dashboard_socket()
    send_command("brake release", dashboard_socket)


def get_safety_status():
    return get_value_from_dashboard("safetystatus")


def get_robot_mode():
    return get_value_from_dashboard("robotmode")


def get_running():
    return get_value_from_dashboard("running")


def get_value_from_dashboard(command: str):
    response = send_command(command, get_dashboard_socket())
    return sanitize_dashboard_reads(response)


def sanitize_dashboard_reads(response: str) -> str:
    message_parts = response.split(":")
    message = message_parts[-1]
    return message.replace('\\n', '').replace(' ', '')


def open_socket(host: str = gethostbyname(gethostname()), port: int = 8000):
    # Todo: Port is duplicate in this method and in open_robot_server, fix it. Cannot import port from websocketProxy, circular imports
    send_command(f"socket_open(\"{host}\", {port}, {SOCKET_NAME})\n", get_interpreter_socket())


def get_interpreter_socket():
    """This function is safe to call multiple times.
    If the interpreter_socket is opened, then it will be returned from cache"""

    global _interpreter_open
    if _interpreter_open:
        return get_socket(POLYSCOPE_IP, _INTERPRETER_PORT)

    power_on_robot()
    brake_release_on_robot()
    start_interpreter_mode()
    sleep(2)

    _interpreter_open = True

    prepare_interpreter_session()

    return get_socket(POLYSCOPE_IP, _INTERPRETER_PORT)


def prepare_interpreter_session():
    # Starting commands we want to send to the robot
    open_socket()
    apply_variables_to_robot(list_of_variables)


def apply_variables_to_robot(variables: list[VariableObject]):
    command = ""
    for variable in variables:
        if variable.variable_type == VariableTypes.String:
            command += f"{variable.name} = \"{variable.value}\" "
        else:
            command += f"{variable.name} = {variable.value} "
    send_command(command, get_interpreter_socket())
    print(f"\t\tVariables applied to robot: {command}")


def sanitize_command(command: str) -> str:
    command = command.replace('\n', ' ')
    command += "\n"  # Add a trailing \n character
    return command


def send_command(command: str, on_socket: Socket, ensure_recovery=False) -> str:
    """Returns the ack_response from the robot. The ack_response is a string."""
    command = sanitize_command(command)
    print(f"Sending the following command: '{escape_string(command)}'")
    on_socket.send(command.encode())
    result = read_from_socket(on_socket)

    if ensure_recovery:
        result = ensure_state_recovery_if_broken(result, command)

    out = ""
    count = 1
    while result != "nothing" and count < 2:
        out += result
        # time_print(f"Received {count}: {escape_string(result)}")
        result = read_from_socket(on_socket)
        count += 1

    return escape_string(out)


# This is a list of variables that are sent to the robot for it to sent it back to the proxy.
list_of_variables: list[VariableObject] = list()
list_of_variables.append(VariableObject("__test__", VariableTypes.Integer, 2))
list_of_variables.append(VariableObject("__test2__", VariableTypes.String, "f"))


def send_user_command(command: CommandMessage, on_socket: Socket) -> str:
    command_message = command.data.command
    response_from_command = send_command(command_message, on_socket, ensure_recovery=True)

    finish_command = CommandFinished(command.data.id, command_message, tuple(list_of_variables))
    string_command = finish_command.dump_ur_string()
    print(f"send_user_command method: String command: {escape_string(string_command)}")
    wrapping = URIFY_return_string(string_command)
    send_command(wrapping, on_socket, ensure_recovery=True)

    test_history(command)

    return response_from_command[:-2]  # Removes \n from the end of the response


class ResponseMessages(Enum):
    Invalid_state = " Program is in an invalid state"
    Ack = "ack"
    Too_many_commands = " Too many interpreted messages"
    Compile_error = " Compile error"
    Syntax_error = " Syntax error"


def ensure_state_recovery_if_broken(response: str, command: str) -> str:
    out = response
    if out == "nothing":
        raise ValueError("Response from robot is nothing. This is not expected.")

    response_array = response.split(":")

    if (ResponseMessages.Ack.value in response_array
            or ResponseMessages.Compile_error.value in response_array
            or ResponseMessages.Syntax_error.value in response_array):
        return out

    # If the robot has interpreted too many commands.
    if ResponseMessages.Too_many_commands.value in response_array:
        print(f"\t\t\tToo many commands detected. Attempting to fix the state.")
        clear_interpreter_mode()
        # Todo: Apply the variables defined by user. Through what the history object has stored.
        apply_variables_to_robot(list_of_variables) # Temporary fix
        return send_command(command, get_interpreter_socket())  # Resend command since it was lost.

    # If the robot is in an invalid state.
    if ResponseMessages.Invalid_state.value in response_array:
        # If the robot is invalid state, we recover state without resending command,
        # since the user still needs the correct feedback.
        safety_status = get_safety_status()
        robot_mode = get_robot_mode()
        running = get_running()
        print(f"\t\t\tResponse from robot: '{response}'")
        print(f"\t\t\tSafety status: '{safety_status}'")

        print(f"\t\t\tRobot mode: '{robot_mode}'")

        print(f"\t\t\tRunning: '{running}'")
        print(f"\t\t\tInvalid state detected. Attempting to fix the state.")
        if safety_status == "NORMAL" and robot_mode == "RUNNING" and running == "false": #Todo read from history instead of dashboard
            print(f"\t\t\tInterpreter mode is stopped, restarting interpreter ")
            restart_interpreter_mode()
            # If the error causing this if to be true is array out of bounds.
            # Then the command is acknowledged but the command_finished is not since the robot
            # goes into an invalid state after it has acknowledged the command that was actually invalid.
            # Therefore, we need to resend the commandfinished message.
            return send_command(command, get_interpreter_socket(), ensure_recovery=True)

    return out


def test_history(command):
    history = History()
    history.new_command(command)
    history.active_command_state().append_state(State())
    history.debug_print()


def read_from_socket(socket: Socket) -> str:
    ready_to_read, ready_to_write, in_error = select.select([socket], [], [], 0.1)
    if ready_to_read:
        message = socket.recv(2048)

        try:
            return message.decode()
        except UnicodeDecodeError as e:
            # Intentionally not returning anything.
            # Returning nothing if a decode error occurs.
            print(f"Error decoding message: {e}")

    return "nothing"


if __name__ == '__main__':
    print("Starting RobotControl.py")
    interpreter_socket: Socket = get_interpreter_socket()

    interpreter_socket.close()
