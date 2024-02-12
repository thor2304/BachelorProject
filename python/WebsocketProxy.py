import asyncio
import sys

from websockets.server import serve
from socket import socket as Socket
from socket import gethostbyname, gethostname, AF_INET, SOCK_STREAM, error
from RobotControl import send_command, get_interpreter_socket

interpreter_socket = get_interpreter_socket("polyscope")

def get_handler(socket: Socket) -> callable:
    async def echo(websocket):
        async for message in websocket:
            print(message)
            send_command(message, socket)

    return echo


async def main():
    task1 = asyncio.create_task(start_webserver())
    task2 = asyncio.create_task(open_and_listen_on_socket())

    await task1
    await task2


async def open_and_listen_on_socket():
    print(f"Starting  ###########################")
    HOST_IP_ADDRESS = gethostbyname(gethostname())
    PORT = 8000

    # create a TCP/IP socket
    server_socket = Socket(AF_INET, SOCK_STREAM)

    try:
        server_socket.bind((HOST_IP_ADDRESS, PORT))
    except error as e:
        print("Error binding the socket: {}".format(e))
        sys.exit(1)

    try:
        server_socket.listen()
    except error as e:
        print("Error listening on the socket: {}".format(e))
        sys.exit(1)

    print("Waiting for a connection...")
    try:
        conn, addr = server_socket.accept()
    except error as e:
        print("Error accepting a connection: {}".format(e))
        sys.exit(1)

    print("Connected to {}".format(addr))
    print_data(conn)

    # async with create_server(('0.0.0.0', 8000)) as server:
    #     print(f"HELLO WORLD")
    #     while True:
    #         print(f"Listening on {server.sockets[0].getsockname()}")
    #         conn, addr = server.accept()
    #
    #         with conn:
    #             print('Connected by', addr)
    #             while True:
    #                 data = conn.recv(1024)
    #                 if not data:
    #                     break
    #                 print(data)


def print_data(socket):
    while True:
        data = socket.recv(1024)
        if not data:
            break
        print(data)


async def start_webserver():
    print("Connecting to interpreter")
    # interpreter_socket: Socket = get_interpreter_socket("polyscope")
    print("Starting websocket server")
    async with serve(get_handler(interpreter_socket), "0.0.0.0", 8767):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())
