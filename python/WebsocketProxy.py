import asyncio
from asyncio import StreamReader, StreamWriter
from time import sleep

from websockets.server import serve
from socket import socket as Socket
from socket import gethostbyname, gethostname, AF_INET, SOCK_STREAM, error
from SocketMessages import parse_command_message, AckResponse, Status
from RobotControl import send_command, get_interpreter_socket, send_wrapped_command, read_from_socket
from ToolBox import time_print

clients = dict()
_START_BYTE = b'\x02'
_END_BYTE = b'\x03'
_EMPTY_BYTE = b''

def get_handler(socket: Socket) -> callable:
    async def echo(websocket):
        async for message in websocket:
            command_message = parse_command_message(message)
            command_string = command_message.data.command
            result = send_wrapped_command(command_message, socket)
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
    sleep(1)
    print(f"Manual delayed read resulted in: {read_from_socket(get_interpreter_socket())}")


def client_connected_cb(client_reader: StreamReader, client_writer: StreamWriter):
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


async def client_task(reader: StreamReader, writer: StreamWriter):
    client_addr = writer.get_extra_info('peername')
    print('Start echoing back to {}'.format(client_addr))
    extra_data = []

    while True:
        data = await reader.read(16)

        if data == _EMPTY_BYTE:
            print('Received EOF. Client disconnected.')
            return

        if extra_data:
            data = extra_data + data
            extra_data = []

        # Check if the data recieved starts with the start byte
        # When using _START_BYTE[0] we return the integer value of the byte in the ascii table, so here it returns 2
        if data[0] != _START_BYTE[0]:
            print(f"Something is WRONG. Data not started with start byte: {data}")

        if _END_BYTE not in data:
            extra_data = data
        else:
            # Split the data into messages within the data
            list_of_data = data.split(_END_BYTE)

            # If the last element is not empty, then it's not the end of the message
            if list_of_data[len(list_of_data) - 1] != _EMPTY_BYTE:
                extra_data = list_of_data.pop()

            for message in list_of_data:
                if message:
                    print(f"Messages decoded: {message.decode()}")


async def start_webserver():
    print("Connecting to interpreter")
    interpreter_socket: Socket = get_interpreter_socket()
    print("Starting websocket server")
    async with serve(get_handler(interpreter_socket), "0.0.0.0", 8767):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())
