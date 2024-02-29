import asyncio
from time import sleep

from websockets.server import serve
from socket import socket as Socket
from socket import gethostbyname, gethostname, AF_INET, SOCK_STREAM, error
from SocketMessages import parse_command_message, AckResponse, Status
from RobotControl import send_command, get_interpreter_socket, send_wrapped_command, read_from_socket
from ToolBox import time_print

clients = dict()


def get_handler(socket: Socket) -> callable:
    async def echo(websocket):
        async for message in websocket:
            command_message = parse_command_message(message)
            command_string = command_message.data.command
            result = send_command(command_string, socket)
            # command = parse_command_message(message)
            # result = send_command(command.data.command, socket)
            # response = AckResponse(command.data.id, command.data.command, result)
            response = AckResponse(command_message.data.id, command_string, result)
            str_response = str(response)
            print(f"Sending response: {str_response}")

            await websocket.send(str_response)

    return echo


async def main():
    print("Starting WebsocketProxy.py")
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(open_robot_server())
        t2 = tg.create_task(start_webserver())
    pass


async def open_robot_server():
    host = '0.0.0.0'
    port = 8000
    srv = await asyncio.start_server(client_connected_cb, host=host, port=port)
    print(f"ip_address of this container: {gethostbyname(gethostname())}")
    async with srv:
        print('server listening for robot connections')
        connect_to_robot_server(gethostbyname(gethostname()), port)
        await srv.serve_forever()


def connect_to_robot_server(host: str, port: int):
    send_command(f"socket_open(\"{host}\", {port})\n", get_interpreter_socket())
    sleep(2)
    print(
        f"Manual delayed read from socket after the socket_open command: {read_from_socket(get_interpreter_socket())}")


def client_connected_cb(client_reader, client_writer):
    # Use peername as client ID
    print("########### We got a customer<<<<<<<<<<<<<")
    client_id = client_writer.get_extra_info('peername')

    print('Client connected: {}'.format(client_id))

    # Define the clean up function here
    def client_cleanup(fu):
        print('Cleaning up client {}'.format(client_id))
        try:  # Retrievre the result and ignore whatever returned, since it's just cleaning
            fu.result()
        except Exception as e:
            pass
        # Remove the client from client records
        del clients[client_id]

    task = asyncio.ensure_future(client_task(client_reader, client_writer))
    task.add_done_callback(client_cleanup)
    # Add the client and the task to client records
    clients[client_id] = task


async def client_task(reader, writer):
    client_addr = writer.get_extra_info('peername')
    print('Start echoing back to {}'.format(client_addr))

    while True:
        data = await reader.read(1024)
        if data == b'':
            print('Received EOF. Client disconnected.')
            return
        else:
            time_print('Backend Received: {}'.format(data.decode()))


async def start_webserver():
    print("Connecting to interpreter")
    interpreter_socket: Socket = get_interpreter_socket()
    print("Starting websocket server")
    async with serve(get_handler(interpreter_socket), "0.0.0.0", 8767):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())
