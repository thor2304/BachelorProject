import socket  # for socket
from socket import socket as Socket
from time import sleep

import select


def get_socket(ip, port):
    print("hello there")
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
    return my_socket


def main():
    print("Starting")
    host_ip: str = "polyscope"
    interpreter_socket: Socket = get_interpreter_socket(host_ip)

    interpreter_socket.close()


def get_interpreter_socket(host_ip: str):
    dashboard_socket = get_socket(host_ip, 29999)
    sleep(5)
    send_command("power on", dashboard_socket)
    sleep(1)
    send_command("brake release", dashboard_socket)
    sleep(1)

    secondary_socket = get_socket(host_ip, 30002)
    send_command("interpreter_mode()", secondary_socket)
    sleep(2)

    # default port for socket
    port: int = 30020

    return get_socket(host_ip, port)


def receive_input_commands(interpreter_socket):
    for i in range(30):
        # print(my_socket.recv(2048))
        action = input('Action?\n')
        send_command(action, interpreter_socket)


def send_test_commands(interpreter_socket):
    send_command("set_digital_out(0, False)\n", interpreter_socket)

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


def send_command(command: str, on_socket: Socket):
    if command.startswith("\n"):
        command = command[1:]
    command = command + '\n' if not command.endswith('\n') else command
    print(f"Sending the following command: '{command.encode('unicode_escape').decode('utf-8')}'")
    on_socket.send(command.encode())
    print(f"Recieved 1st: {read_from_socket(on_socket)}")
    print(f"Recieved 2nd: {read_from_socket(on_socket)}")


def read_from_socket(socket: Socket):
    ready_to_read, ready_to_write, in_error = select.select([socket], [], [], 1)
    if ready_to_read:
        return socket.recv(2048)
    return "nothing"


if __name__ == '__main__':
    main()
