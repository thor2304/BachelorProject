import socket  # for socket
from socket import socket as Socket
from time import sleep


def get_socket(ip, port):
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

    send_command("test()\n", interpreter_socket)

    send_command('popup("post","post")', interpreter_socket)


def send_command(command: str, on_socket: Socket):
    command = command + '\n' if not command.endswith('\n') else command
    on_socket.send(command.encode())
    print(f"Recieved: {on_socket.recv(2048)}")


if __name__ == '__main__':
    main()
