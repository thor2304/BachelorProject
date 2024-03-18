import json
from enum import Enum, auto


class RobotSocketMessageTypes(Enum):
    Command_finished = auto()
    Report_state = auto()


class VariableTypes(Enum):
    """
    This is a list of variable types that can be sent to the robot
    Each type has a corresponding character that is used to identify the type
    """
    String = "<"
    Integer = "|"
    Float = "@"
    Boolean = "£"
    List = "?"
    Pose = "!"


class VariableObject:
    def __init__(self, name: str, variable_type: VariableTypes,
                 value: str | int | float | bool | list | tuple[float, float, float, float, float, float]):
        self.name = name
        self.variable_type = variable_type
        self.value = value

    def dump(self, ur_prep=False):
        value = self.value if not ur_prep else f'\"\"{self.variable_type.value}{self.value}\"\"'
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
            "data": [variable.dump(True) for variable in self.variables]
        }

    def dump_ur_string(self):
        return json.dumps(self.dump())
