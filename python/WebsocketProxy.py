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
    task1 = asyncio.create_task(start_webserver())
    task2 = asyncio.create_task(hello())

    await task1
    await task2


async def hello():
    while True:
        await asyncio.sleep(2)
        print("Hello")


async def start_webserver():
    print("Connecting to interpreter")
    interpreter_socket: Socket = get_interpreter_socket("polyscope")
    print("Starting websocket server")
    async with serve(get_handler(interpreter_socket), "0.0.0.0", 8767):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())
