import asyncio
from websockets.server import serve
from socket import socket as Socket
from RobotControl import send_command, get_interpreter_socket


def get_handler(socket: Socket) -> callable:
    async def echo(websocket):
        async for message in websocket:
            print(message)
            send_command(message, socket)

    return echo


async def main():
    interpreter_socket: Socket = get_interpreter_socket("localhost")
    print("Starting websocket server")
    async with serve(get_handler(interpreter_socket), "localhost", 8765):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())
