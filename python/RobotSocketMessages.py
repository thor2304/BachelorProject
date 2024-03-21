import json
from enum import Enum, auto

from RobotSocketVariableTypes import VariableTypes
from URIFY import URIFY_return_string


class RobotSocketMessageTypes(Enum):
    Command_finished = auto()
    Report_state = auto()


class VariableObject:
    def __init__(self, name: str, variable_type: VariableTypes,
                 value: str | int | float | bool | list | tuple[float, float, float, float, float, float]):
        self.name = name
        self.variable_type = variable_type
        self.value = value

    def dump(self, ur_prep=False):
        value = self.value if not ur_prep else f'\"\"{self.variable_type.value}{self.name}\"\"'
        return {
            "name": self.name,
            "type": self.variable_type.name,
            "value": value
        }

    def dump_ur_string_for_report_state(self):
        value = f'\"\"{self.variable_type.value}{self.value}\"\"'
        return {
            "name": self.name,
            "type": self.variable_type.name,
            "value": value
        }

    def __str__(self):
        return json.dumps(self.dump())


class CommandFinishedData:
    def __init__(self, id: int, command: str, variables: tuple[VariableObject, ...]):
        self.id = id
        self.command = command
        self.variables = variables


class CommandFinished:
    def __init__(self, id: int, command: str, variables: tuple[VariableObject, ...]):
        self.type = RobotSocketMessageTypes.Command_finished
        self.data: CommandFinishedData = CommandFinishedData(id, command, variables)

    # Issue later should handle the case where the command contains a comment
    def command_contains_comment(self):
        if "#" in self.data.command:
            return True
        return False

    def __str__(self):
        if self.command_contains_comment():
            raise ValueError("Command contains comment")

        return json.dumps(self.dump())

    def dump(self, ur_prep=False):
        return {
            "type": self.type.name,
            "data": {
                "id": self.data.id,
                "command": self.data.command,
                "variables": [variable.dump(ur_prep) for variable in self.data.variables]
            }
        }

    def dump_ur_string(self):
        return json.dumps(self.dump(True))


class ReportState:
    def __init__(self, variables: list[VariableObject]):
        self.type = RobotSocketMessageTypes.Report_state
        self.variables: list[VariableObject] = variables

    def __str__(self):
        return json.dumps(self.dump())

    def dump(self):
        return {
            "type": self.type.name,
            "data": [variable.dump_ur_string_for_report_state() for variable in self.variables]
        }

    def dump_string_pre_urify(self):
        return json.dumps(self.dump())

    def dump_string_post_urify(self):
        return URIFY_return_string(self.dump_string_pre_urify())


def parse_list_to_variable_objects(variable_list: list[dict]) -> list[VariableObject]:
    out: list[VariableObject] = list()
    for variable in variable_list:
        match variable:
            case {
                'name': name,
                'type': variable_type,
                'value': value
            }:
                out.append(VariableObject(name, VariableTypes[variable_type], value))
            case _:
                raise ValueError(f"Unknown VariableObject type: {variable}")
    return out


def parse_robot_message(message: str) -> CommandFinished | ReportState:
    parsed = json.loads(message)

    match parsed:
        case {
            'type': RobotSocketMessageTypes.Report_state.name,
            'variables': variable_list
        }:
            parsed_variable_list = parse_list_to_variable_objects(variable_list)
            return ReportState(parsed_variable_list)
        case {
            'type': RobotSocketMessageTypes.Command_finished.name,
            'data': {
                'id': id,
                'command': command,
                'variables': variable_list
            }
        }:
            parsed_variable_list = parse_list_to_variable_objects(variable_list)
            return CommandFinished(id, command, tuple(parsed_variable_list))
        case _:
            raise ValueError(f"Unknown RobotSocketMessage type: {parsed}")

