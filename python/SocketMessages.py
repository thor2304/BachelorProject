import json
from builtins import list
from enum import Enum, auto


class MessageType(Enum):
    Command = auto()
    Ack_response = auto()
    Feedback = auto()
    Robot_state = auto()


class Status(Enum):
    Ok = auto()
    Error = auto()

    @classmethod
    def parse(cls, message: str):
        if message.startswith("ack:"):
            return cls.Ok
        elif message.startswith("discard:"):
            return cls.Error
        else:
            raise ValueError(f"Unknown status message: {message}")


class CommandMessageData:
    def __init__(self, id: int, command: str):
        self.id = id
        self.command = command


class AckResponseData:
    def __init__(self, id: int, status: Status, command: str, message: str):
        self.id = id
        self.status = status
        self.command = command
        self.message = message


class FeedbackData:
    def __init__(self, id: int, message: str):
        self.id = id
        self.message = message


class RobotStateData:
    def __init__(self, state: str, joints: list[int, int, int, int, int, int]):
        self.state = state
        self.joints = joints


class CommandMessage:
    def __init__(self, id: int, command: str):
        self.type = MessageType.Command
        self.data: CommandMessageData = CommandMessageData(id, command)


class AckResponse:
    def __init__(self, id: int, command: str, message: str):
        self.type = MessageType.Ack_response
        self.data: AckResponseData = AckResponseData(id, Status.parse(message), command, message)

    def __str__(self):
        return json.dumps({
            "type": self.type.name,
            "data": {
                "id": self.data.id,
                "status": self.data.status.name,
                "command": self.data.command,
                "message": self.data.message
            }
        })


class Feedback:
    def __init__(self, id: int, message: str):
        self.type = MessageType.Feedback
        self.data: FeedbackData = FeedbackData(id, message)


class RobotState:
    def __init__(self, state: str, joints: list[int, int, int, int, int, int]):
        self.type = MessageType.Robot_state
        self.data: RobotStateData = RobotStateData(state, joints)


def parse_command_message(message: str) -> CommandMessage:
    parsed = json.loads(message)
    if parsed["type"] != MessageType.Command.name:
        raise ValueError(f"Message type: {parsed['type']} is not of type Command {MessageType.Command.name}")
    return CommandMessage(parsed["data"]["id"], parsed["data"]["command"])
