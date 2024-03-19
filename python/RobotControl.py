import socket  # for socket
from socket import socket as Socket
from time import sleep
from typing import Callable

import select

from RobotSocketMessages import CommandFinished, VariableObject, VariableTypes
from SocketMessages import CommandMessage
from ToolBox import escape_string, time_print
from undo.History import History
from undo.State import State

POLYSCOPE_IP = "polyscope"


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


def get_interpreter_socket():
    """This function is safe to call multiple times.
    If the interpreter_socket is opened, then it will be returned from cache"""
    # default port for socket
    interpreter_port: int = 30020

    global _interpreter_open
    if _interpreter_open:
        return get_socket(POLYSCOPE_IP, interpreter_port)

    dashboard_socket = get_socket(POLYSCOPE_IP, 29999)
    # sleep(5)
    send_command("power on", dashboard_socket)
    # sleep(1)
    send_command("brake release", dashboard_socket)
    # sleep(1)

    secondary_socket = get_socket(POLYSCOPE_IP, 30002)
    send_command("interpreter_mode()", secondary_socket)
    sleep(2)

    _interpreter_open = True

    interpreter_socket = get_socket(POLYSCOPE_IP, interpreter_port)

    prepare_interpreter_session(interpreter_socket)

    return interpreter_socket


def prepare_interpreter_session(interpreter_socket: Socket):
    ## Starting commands we want to send to the robot
    send_command("__test__ = 2", interpreter_socket)
    send_command("__test2__ = \"f\"", interpreter_socket)


def get_rtde_socket():
    return get_socket(POLYSCOPE_IP, 30004)


def receive_input_commands(interpreter_socket: Socket):
    for i in range(30):
        # print(my_socket.recv(2048))
        action = input('Action?\n')
        send_command(action, interpreter_socket)


def send_test_commands(interpreter_socket: Socket):
    send_wrapped_command("set_digital_out(0, False)\n", interpreter_socket)

    send_command("set_digital_out(1, False)\n", interpreter_socket)
    send_command("set_digital_out(2, False)\n", interpreter_socket)

    send_command("b=0\n", interpreter_socket)

    send_command("set_digital_out(b, True)\n", interpreter_socket)

    function_def: str = (
        "def test():\n"
        "a = True\n"
        "set_digital_out(2, a)\n"
        "set_digital_out(1, True)\n"
        "end\n"
        "test()\n"
    )

    # send_command(function_def, my_socket)

    function_def_no_new_line = (
        "def test():"
        " out = "
        " set_digital_out(2, a)                                                      "
        " set_digital_out(1, True) "
        " end "
        " test()\n"
    )
    send_command(function_def_no_new_line, interpreter_socket)

    function_connect_to_socket = (
        'socket_open("proxy","8000")\n'
        'def send(id):'
        'out = "{\\"type\\": \\"Command\\", \\"data\\": {\\"id\\": " + id + ", \\"var1\\": " + var1 + "}}"'
        'socket_send_string(out)'
        'end'
        'thread sending():'
        'while True:'
        'send(10)'
        'end'
        'end'
    )

    send_command("test()\n", interpreter_socket)

    send_command('popup("post","post")', interpreter_socket)


def sanitize_command(command: str) -> str:
    command = command.replace('\n', ' ')
    command += "\n" # Add a trailing \n character
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
    print(f"String command: {string_command}")
    wrapping = URIFY_return_string(string_command)
    command_message += wrapping

    extra_len = len(wrapping) + 1  # the 1 is to remove the trailing \n character

    history = History()
    history.new_command(command)
    history.active_command_state().append_state(State())
    history.debug_print()
    response = send_command(command_message, on_socket)

    return response[0:-extra_len]


def URIFY_return_string(string_to_urify: str) -> str:
    """
    This function takes a string and returns a string that can be sent to the robot and then sent back to the proxy.\n
    The function does this by replacing all the quotes with socket_send_byte(34).\n
    For values of variables sent, the function ensures that the variable's value is not quoted, so the robot returns the
    actual value of the variable.

    :param string_to_urify: The string to be URIFYed for sending to the robot

    :return: The URIFYed string that can be sent to the robot
    """

    out = " socket_send_byte(2) "  # Start byte

    list_of_strings = string_to_urify.split('\\"\\"')

    for i in range(0, len(list_of_strings)):
        if i % 2 == 0:
            sub_string: str = list_of_strings[i]
            if i < len(list_of_strings) - 1:
                sub_string = sub_string[:-1]
            if i > 0:
                sub_string = sub_string[1:]

            out += _urify_string(sub_string)
        else:
            out += create_socket_send_string_variable(list_of_strings[i])

    out += " socket_send_byte(3) "  # End byte
    return out


def _urify_string(string: str) -> str:
    urified_string = ""

    # Split the string by quotes
    between_quotes = string.split('"')
    if len(between_quotes) == 1:
        return create_socket_send_string(string)

    first = between_quotes.pop(0)
    if first != "":
        urified_string += create_socket_send_string(first)
    else:
        urified_string += create_quote_send()

    for part in between_quotes:
        if part == "":
            continue

        urified_string += create_quote_send()
        urified_string += create_socket_send_string(part)

    return urified_string


def create_socket_send_string_variable(string_to_send: str) -> str:
    if string_to_send == "":
        return ""

    wrap_in_quotes = False
    start_char = string_to_send[0]

    match start_char:
        case VariableTypes.String.value:
            string_to_send = string_to_send[1:]
            wrap_in_quotes = True
        case VariableTypes.Integer.value | VariableTypes.Float.value | VariableTypes.Boolean.value | VariableTypes.List.value | VariableTypes.Pose.value:
            string_to_send = string_to_send[1:]
        case _:
            pass

    out = f" socket_send_string({string_to_send}) "

    if wrap_in_quotes:
        out = create_quote_send() + out + create_quote_send()

    return out


def create_socket_send_string(string_to_send: str) -> str:
    if string_to_send == "":
        return ""
    return f" socket_send_string(\"{string_to_send}\") "


def create_quote_send() -> str:
    return " socket_send_byte(34) "


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
