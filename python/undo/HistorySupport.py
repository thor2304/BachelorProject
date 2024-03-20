import asyncio

from RobotControl import get_interpreter_socket, send_command
from RobotSocketMessages import ReportState
from undo.VariableRegistry import VariableRegistry

_variable_registry = VariableRegistry()

READ_FREQUENCY_HZ = 1
READ_PERIOD = 1 / READ_FREQUENCY_HZ


def read_variable_state():
    interpreter_socket = get_interpreter_socket()
    read_commands = _variable_registry.generate_read_commands()
    report_state = ReportState(read_commands)
    send_command(report_state.dump_ur_string(), interpreter_socket)


async def start_read_loop():
    while True:
        read_variable_state()
        await asyncio.sleep(READ_PERIOD)
