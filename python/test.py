from RobotControl import send_command, get_interpreter_socket, send_wrapped_command
from socket import socket as Socket


def test():
    socket: Socket = get_interpreter_socket()

    commands = [
        "movej([0.0, 1.57, 0.0, -1.57, 0.0, 0.0], a=1.4, v=1.05)",
        "set_digital_out(0, True)",
        "set_digital_out(1, False)",
        "set_digital_out(2, True)",
        "set_digital_out(3, True)",
        "popup(\"post\",\"post\")"
    ]

    for command in commands:
        send_wrapped_command(command, socket)

if __name__ == '__main__':
    test()