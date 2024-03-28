import asyncio
from asyncio import StreamReader, StreamWriter, Task
from socket import gethostbyname, gethostname
from socket import socket as Socket
from time import sleep
from typing import Final

from websockets.server import serve

from RobotControl import get_interpreter_socket, send_user_command, power_on_robot, brake_release_on_robot, \
    get_robot_mode, start_interpreter_mode_and_connect_to_backend_socket, read_from_socket_till_end
from SocketMessages import AckResponse
from SocketMessages import parse_message, CommandMessage, UndoMessage, UndoResponseMessage, UndoStatus
from RobotSocketMessages import parse_robot_message, CommandFinished, ReportState
from ToolBox import escape_string
from WebsocketNotifier import websocket_notifier

clients = dict()
_START_BYTE: Final = b'\x02'
_END_BYTE: Final = b'\x03'
_EMPTY_BYTE: Final = b''

_connected_web_clients = set()


def handle_command_message(message: CommandMessage, socket: Socket) -> str:
    command_string = message.data.command
    result = send_user_command(message, socket)
    response = AckResponse(message.data.id, command_string, result)
    str_response = str(response)
    print(f"Sending response: {str_response}")
    return str_response


def handle_undo_message(message: UndoMessage) -> str:
    response = UndoResponseMessage(message.data.id, UndoStatus.Success)
    print(f"Sending response: {response}")
    return str(response)


def get_handler(socket: Socket) -> callable:
    async def echo(websocket):
        _connected_web_clients.add(websocket)
        async for message in websocket:
            print(f"Received message: {message}")

            message = parse_message(message)

            match message:
                case CommandMessage():
                    str_response = handle_command_message(message, socket)
                    print(f"Message is a CommandMessage")
                case UndoMessage():
                    str_response = handle_undo_message(message)
                    print(f"Message is an UndoMessage")
                case _:
                    raise ValueError(f"Unknown message type: {message}")

            await websocket.send(str_response)

    return echo


def send_to_all_web_clients(message: str):
    # We need to use list() around connected web clients to prevent: RuntimeError: Set changed size during iteration
    # The exception occurred when you refreshed the web and send a new command.
    for websocket in list(_connected_web_clients):
        if websocket.closed:
            _connected_web_clients.remove(websocket)
            continue
    for websocket in _connected_web_clients:
        asyncio.create_task(websocket.send(message))


# To prevent circular dependencies
websocket_notifier.register_observer(send_to_all_web_clients)


async def open_robot_server():
    host = '0.0.0.0'
    port = 8000
    srv = await asyncio.start_server(client_connected_cb, host=host, port=port)
    print(f"ip_address of this container: {gethostbyname(gethostname())}")
    async with srv:
        print('server listening for robot connections')
        await srv.serve_forever()


def client_connected_cb(client_reader: StreamReader, client_writer: StreamWriter):
    # Use peername as client ID
    print("########### We got a customer<<<<<<<<<<<<<")
    client_id = client_writer.get_extra_info('peername')

    print('Client connected: {}'.format(client_id))

    # Define the cleanup function here
    def client_cleanup(fu: Task[None]):
        print('Cleaning up client {}'.format(client_id))
        try:  # Retrieve the result and ignore whatever returned, since it's just cleaning
            fu.result()
        except Exception as e:
            raise e
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
        data = await reader.read(4096)
        if data:
            print(f"BACKEND recieved data from client: {data}")

        if data == _EMPTY_BYTE:
            print('Received EOF. Client disconnected.')
            return

        if extra_data:
            data = extra_data + data
            extra_data = []

        # Check if the data received starts with the start byte
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
                    message = message[1:]  # remove the start byte
                    message_from_robot_received(message)


def message_from_robot_received(message: bytes):
    decoded_message = message.decode()
    print(f"Message from robot: {decoded_message}")
    robot_message = parse_robot_message(decoded_message)
    print(f"Robot message: {robot_message}")
    match robot_message:
        case CommandFinished():
            send_to_all_web_clients(str(robot_message))
        case ReportState():
            print(f"Messaged decoded to be a ReportState: {robot_message.dump()}")
        case _:
            raise ValueError(f"Unknown RobotSocketMessage message: {robot_message}")


async def start_webserver():
    ensure_polyscope_is_ready()
    print(f"Polyscope is ready. The robot mode is: {get_robot_mode()}")

    power_on_robot()
    brake_release_on_robot()
    start_interpreter_mode_and_connect_to_backend_socket()

    interpreter_socket: Socket = get_interpreter_socket()
    print("Starting websocket server")
    async with serve(get_handler(interpreter_socket), "0.0.0.0", 8767):
        await asyncio.Future()  # run forever


def ensure_polyscope_is_ready():
    robot_mode = get_robot_mode()
    rerun = False
    if robot_mode == '' or robot_mode == 'BOOTING':
        print(f"Polyscope is still starting: {robot_mode}")
        rerun = True

    # UniversalRobotsDashboardServer is a not documented state, but it is a state that the robot can be in
    if robot_mode == 'NO_CONTROLLER' or robot_mode == 'DISCONNECTED' or robot_mode == 'UniversalRobotsDashboardServer':
        print(f"Polyscope is in current state of starting: {robot_mode}")
        rerun = True

    if rerun:
        sleep(0.1)
        ensure_polyscope_is_ready()
