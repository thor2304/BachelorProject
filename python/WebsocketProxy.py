import asyncio
import sys

from websockets.server import serve
from socket import socket as Socket
from socket import gethostbyname, gethostname, AF_INET, SOCK_STREAM, error
from RobotControl import send_command, get_interpreter_socket

interpreter_socket = get_interpreter_socket("polyscope")

clients = dict()


def get_handler(socket: Socket) -> callable:
    async def echo(websocket):
        async for message in websocket:
            print(message)
            send_command(message, socket)

    return echo


async def main():
    host = 'localhost'
    port = 8000
    loop = asyncio.get_event_loop()
    
    server_coro = asyncio.start_server(client_connected_cb,
                                       host=host,
                                       port=port,
                                       loop=loop)
    print("Starting server")
    server = loop.run_until_complete(server_coro)
    print("Server started")
    print('Starting proxy...')
    loop.run_until_complete(start_webserver())
    print('Proxy started')

    try:
        print('Serving on {}:{}'.format(host, port))
        loop.run_forever()
    except KeyboardInterrupt as e:
        print('Keyboard interrupted. Exit.')
    # Close the server
    server.close()
    print('Server closed')
    loop.run_until_complete(server.wait_closed())
    loop.close()


def client_connected_cb(client_reader, client_writer):
    # Use peername as client ID
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
            print('Received: {}'.format(data.decode()))


# async def open_and_listen_on_socket():
#     print(f"Starting  ###########################")
#     HOST_IP_ADDRESS = gethostbyname(gethostname())
#     PORT = 8000
#
#     # create a TCP/IP socket
#     server_socket = Socket(AF_INET, SOCK_STREAM)
#
#     try:
#         server_socket.bind((HOST_IP_ADDRESS, PORT))
#     except error as e:
#         print("Error binding the socket: {}".format(e))
#         sys.exit(1)
#
#     try:
#         server_socket.listen()
#     except error as e:
#         print("Error listening on the socket: {}".format(e))
#         sys.exit(1)
#
#     print("Waiting for a connection...")
#     try:
#         conn, addr = server_socket.accept()
#     except error as e:
#         print("Error accepting a connection: {}".format(e))
#         sys.exit(1)
#
#     print("Connected to {}".format(addr))
#     print_data(conn)


# def print_data(socket):
#     while True:
#         data = socket.recv(1024)
#         if not data:
#             break
#         print(data)


async def start_webserver():
    print("Connecting to interpreter")
    # interpreter_socket: Socket = get_interpreter_socket("polyscope")
    print("Starting websocket server")
    async with serve(get_handler(interpreter_socket), "0.0.0.0", 8767):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())
