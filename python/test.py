from python.RobotControl import get_socket


def test():
    robot_server_socket = get_socket('localhost', 8000)
    robot_server_socket.setblocking(True)
    robot_server_socket.send(b'Hello from test.py')
    print(robot_server_socket.recv(2048))

if __name__ == '__main__':
    test()