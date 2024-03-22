import asyncio

from rtde.serialize import DataObject

from RobotControl import get_interpreter_socket, send_command
from RobotSocketMessages import ReportState
from SocketMessages import RobotState
from undo.History import History
from undo.State import State, StateType
from undo.StateValue import StateValue
from undo.VariableRegistry import VariableRegistry, register_all_code_variables, register_all_rtde_variables

_variable_registry = VariableRegistry()

READ_FREQUENCY_HZ = 1
READ_PERIOD = 1 / READ_FREQUENCY_HZ


def get_variable_registry():
    return _variable_registry


def create_state_from_rtde_state(state: DataObject) -> State:
    state_values: list[StateValue] = []
    robot_state = RobotState(state)

    rtde_variables = get_variable_registry().get_rtde_variables()

    received_variables = robot_state.data.dump()

    for variable_definition in rtde_variables:
        try:
            variable_value = received_variables[variable_definition.rtde_variable_name]
        except KeyError:
            raise ValueError(
                f"Variable {variable_definition.name} not found in received state,"
                f" with keys: {received_variables.keys()}")
        if variable_value is None:
            raise ValueError(
                f"Variable {variable_definition.name} not found in received state,"
                f" with keys: {received_variables.keys()}")

        state_values.append(StateValue(variable_value, variable_definition))

    if len(state_values) != len(received_variables):
        raise ValueError(f"Received state has {len(received_variables)} variables,"
                         f" but only {len(state_values)} were processed.")

    return State(StateType.rtde_state, state_values)


def register_all_variables():
    register_all_code_variables(_variable_registry)
    register_all_rtde_variables(_variable_registry)


register_all_variables()


def read_variable_state():
    print("Reading variable state")
    interpreter_socket = get_interpreter_socket()
    read_commands = _variable_registry.generate_read_commands()
    report_state = ReportState(read_commands)
    send_command(report_state.dump_string_post_urify(), interpreter_socket)


async def start_read_loop():
    while True:
        read_variable_state()
        await asyncio.sleep(READ_PERIOD)


def create_state_from_report_state(report_state: ReportState) -> State:
    state_values: list[StateValue] = []

    code_variables = get_variable_registry().get_code_variable_dict()

    received_variables = report_state.variables

    for variable in received_variables:
        variable_name = variable.name
        if variable_name not in code_variables:
            raise ValueError(f"Variable {variable_name} not found in code variables")
        code_variable = code_variables[variable_name]
        state_values.append(StateValue(variable.value, code_variable))

    if len(state_values) != len(received_variables):
        raise ValueError(f"Received state has {len(received_variables)} variables,"
                         f" but only {len(state_values)} were processed.")

    return State(StateType.code_state, state_values)


def handle_report_state(reported_state: ReportState):
    state = create_state_from_report_state(reported_state)
    history = History.get_history()
    history.append_state(state)
    print(f"Received state: {state}")
