import json
from enum import Enum, auto


class RobotSocketMessageTypes(Enum):
    Command_finished = auto()


class VariableTypes(Enum):
    String = auto()
    Integer = auto()
    Float = auto()
    Boolean = auto()
    List = auto()
    Pose = auto()


class VariableObject:
    def __init__(self, name: str, variable_type: VariableTypes,
                 value: str | int | float | bool | list | tuple[float, float, float, float, float, float]):
        self.name = name
        self.variable_type = variable_type
        self.value = value

    def dump(self):
        return {
            "name": self.name,
            "type": self.variable_type.name,
            "value": self.value
        }


class CommandFinishedData:
    def __init__(self, id: int, command: str, variables: tuple[VariableObject, ...]):
        self.id = id
        self.command = command
        self.variables = variables


class CommandFinished:
    def __init__(self, id: int, command: str, variables: tuple[VariableObject, ...]):
        self.type = RobotSocketMessageTypes.Command_finished
        self.data: CommandFinishedData = CommandFinishedData(id, command, variables)

    def __str__(self):
        return json.dumps({
            "type": self.type.name,
            "data": {
                "id": self.data.id,
                "command": self.data.command,
                "variables": [variable.dump() for variable in self.data.variables]
            }
        })

