import socket  # for socket
from socket import socket as Socket
from time import sleep
from typing import Callable

import select

from RobotSocketMessages import CommandFinished, VariableObject, VariableTypes
from SocketMessages import CommandMessage

POLYSCOPE_IP = "polyscope"

from ToolBox import escape_string, time_print


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


def main():
    print("Starting RobotControl.py")
    interpreter_socket: Socket = get_interpreter_socket()

    interpreter_socket.close()


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


def send_command(command: str, on_socket: Socket) -> str:
    if command.startswith("\n"):
        command = command[1:]
    command = command + '\n' if not command.endswith('\n') else command
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


def send_wrapped_command(command: CommandMessage, on_socket: Socket) -> str:
    command_message = command.data.command
    if command_message.endswith('\n'):
        command_message = command_message[:-1]

    finish_command = CommandFinished(command.data.id, command_message, tuple(list_of_variables))
    string_command = finish_command.dump_string()
    wrapping = URIFY_return_string(string_command)
    command_message += wrapping

    extra_len = len(wrapping) + 1  # the 1 is to remove the trailing \n character

    response = send_command(command_message, on_socket)
    # Sending it twice to test backend reading
    send_command(command_message, on_socket)

    return response[0:-extra_len]


def URIFY_return_string(input: str) -> str:
    """
    This function takes a string and returns a string that can be sent to the robot and then sent back to the proxy.\n
    The function does this by replacing all the quotes with socket_send_byte(34).\n
    For values of variables sent, the function ensures that the variable's value is not quoted, so the robot returns the
    actual value of the variable.

    :param input: The string to be URIFYed for sending to the robot

    :return: The URIFYed string that can be sent to the robot
    """

    # Variables to keep track of where we are in the string
    var_name: str = ""
    count = 0

    # Split the string by quotes
    between_quotes = input.split('"')
    if len(between_quotes) == 1:
        return create_socket_send_string(input)

    # The first part of the string is not between quotes, so we can just pop it off
    first = between_quotes.pop(0)
    out = " socket_send_byte(2) "

    out += create_socket_send_string(first)
    for part in between_quotes:
        if part == "name" and count < 1:  # count < 1 is to make sure that variable named name and value still work
            count = 4
        if part == "value" and count < 1:  # count < 1 is to make sure that variable named name and value still work
            count = 4
        count -= 1
        if count == 1:
            if var_name == "":
                var_name = part
                out += create_quote_send()
                out += create_socket_send_string(part)
            else:
                out += create_socket_send_string_no_quotes(var_name)
                print(f"Setting variable name: {var_name}")
                var_name = ""
        elif count == 0:
            if var_name != "":
                out += create_quote_send()
            out += create_socket_send_string(part)
        else:
            out += create_quote_send()
            out += create_socket_send_string(part)

    out += " socket_send_byte(3) "
    return out


def create_socket_send_string_no_quotes(string_to_send: str) -> str:
    if string_to_send == "":
        return ""
    return f" socket_send_string({string_to_send}) "


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
    main()
