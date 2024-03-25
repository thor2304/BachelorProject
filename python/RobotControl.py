import socket  # for socket
from socket import socket as Socket
from time import sleep
from typing import Callable

import select

from RobotSocketMessages import CommandFinished, VariableObject, VariableTypes
from SocketMessages import CommandMessage
from ToolBox import escape_string, time_print
from URIFY import URIFY_return_string
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
    send_command("interpreter_mode()", secondary_socket)


def power_on_robot():
    dashboard_socket = get_dashboard_socket()
    send_command("power on", dashboard_socket)


def brake_release_on_robot():
    dashboard_socket = get_dashboard_socket()
    send_command("brake release", dashboard_socket)


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
    interpreter_socket = get_socket(POLYSCOPE_IP, _INTERPRETER_PORT)
    # Starting commands we want to send to the robot
    send_command("__test__ = 2", interpreter_socket)
    send_command("__test2__ = \"f\"", interpreter_socket)


def sanitize_command(command: str) -> str:
    command = command.replace('\n', ' ')
    command += "\n"  # Add a trailing \n character
    return command


def send_command(command: str, on_socket: Socket) -> str:
    """Returns the ack_response from the robot. The ack_response is a string."""
    command = sanitize_command(command)
    print(f"Sending the following command: '{escape_string(command)}'")
    on_socket.send(command.encode())
    result = read_from_socket(on_socket)
    out = ""
    count = 1
    while result != "nothing" and count < 2:
        out += result
        time_print(f"Received {count}: {escape_string(result)}")
        result = read_from_socket(on_socket)
        count += 1

    return escape_string(out)


# This is a list of variables that are sent to the robot for it to sent it back to the proxy.
list_of_variables: list[VariableObject] = list()
list_of_variables.append(VariableObject("__test__", VariableTypes.Integer, 2))
list_of_variables.append(VariableObject("__test2__", VariableTypes.String, "f"))


def send_user_command(command: CommandMessage, on_socket: Socket) -> str:
    command_message = command.data.command
    finish_command = CommandFinished(command.data.id, command_message, tuple(list_of_variables))
    string_command = finish_command.dump_ur_string()
    print(f"send_user_command method: String command: {string_command}")
    wrapping = URIFY_return_string(string_command)

    test_history(command)
    response = send_command(command_message, on_socket)
    send_command(wrapping, on_socket)

    return response[:-2]  # Removes \n from the end of the response


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
