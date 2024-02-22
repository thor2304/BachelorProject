import socket  # for socket
from socket import socket as Socket
from time import sleep
from typing import Callable

import select

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
    # default port for socket
    interpreter_port: int = 30020

    global _interpreter_open
    if _interpreter_open:
        return get_socket(POLYSCOPE_IP, interpreter_port)

    dashboard_socket = get_socket(POLYSCOPE_IP, 29999)
    sleep(5)
    send_command("power on", dashboard_socket)
    sleep(1)
    send_command("brake release", dashboard_socket)
    sleep(1)

    secondary_socket = get_socket(POLYSCOPE_IP, 30002)
    send_command("interpreter_mode()", secondary_socket)
    sleep(2)

    _interpreter_open = True

    return get_socket(POLYSCOPE_IP, interpreter_port)


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
        " a = True "
        " set_digital_out(2, a)                                                      "
        " set_digital_out(1, True) "
        " end "
        " test()\n"
    )
    send_command(function_def_no_new_line, interpreter_socket)

    function_connect_to_socket = (
        'socket_open("proxy","8000")\n'
        'socket_send_string("Hello from UR")\n'
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
        time_print(f"Recieved {count}: {escape_string(result)}")
        result = read_from_socket(on_socket)
        count += 1

    return escape_string(out)


def send_wrapped_command(command: str, on_socket: Socket) -> str:
    if command.endswith('\n'):
        command = command[:-1]
    command += ' socket_send_string(\"Finished sending command\")'
    return send_command(command, on_socket)


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
