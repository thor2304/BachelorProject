import json
from builtins import list
from enum import Enum, auto
from rtde.serialize import DataObject


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


class JointState:
    def __init__(self, q_actual: list[float, float, float, float, float, float]):
        self.base = q_actual[0]
        self.shoulder = q_actual[1]
        self.elbow = q_actual[2]
        self.wrist1 = q_actual[3]
        self.wrist2 = q_actual[4]
        self.wrist3 = q_actual[5]

    def __getitem__(self, item) -> float:
        if item == 0:
            return self.base
        elif item == 1:
            return self.shoulder
        elif item == 2:
            return self.elbow
        elif item == 3:
            return self.wrist1
        elif item == 4:
            return self.wrist2
        elif item == 5:
            return self.wrist3
        else:
            raise ValueError(f"Unknown joint index: {item}")


class StatusTypes(Enum):
    normal_mode = 0
    reduced_mode = 1
    protective_stop = 2
    recovery_mode = 3
    safeguard_stop = 4
    system_emergency_stop = 5
    robot_emergency_stop = 6
    emergency_stopped = 7
    violation = 8
    fault = 9
    stopped_due_to_safety = 10


lookup_state_types: dict[int, StatusTypes] = {element.value: element for element in StatusTypes}


class RobotStateData:
    def __init__(self, status: StatusTypes, joints: JointState):
        self.status: StatusTypes = status
        self.joints: JointState = joints

    def dump(self):
        return {
            "status": self.status.name,
            "joints": [self.joints.base, self.joints.shoulder, self.joints.elbow,
                       self.joints.wrist1, self.joints.wrist2, self.joints.wrist3]
        }


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


class TransmittedInformationOptions(Enum):
    state = "safety_status_bits"
    joints = "actual_q"


def raise_exception_when_called():
    raise ValueError("Invalid argument")


class RobotState:
    def __init__(self, state: DataObject):
        self.type = MessageType.Robot_state
        status: StatusTypes = ensure_type_of_status(state.__getattribute__(TransmittedInformationOptions.state.value))
        joints: JointState = ensure_type_of_joints(state.__getattribute__(TransmittedInformationOptions.joints.value))
        self.data: RobotStateData = RobotStateData(status, joints)

    def __str__(self):
        return json.dumps({
            "type": self.type.name,
            "data": self.data.dump()
        })


def ensure_type_of_status(status: any) -> StatusTypes:
    if not isinstance(status, int):
        raise ValueError(f"Status is not of type int: {status}")
    if status not in lookup_state_types:
        raise ValueError(f"Status is not a known state: {status}")
    return lookup_state_types[status]


def ensure_type_of_joints(joints: any) -> JointState:
    if not isinstance(joints, list):
        raise ValueError(f"Joints are not of type list: {joints}")
    if len(joints) != 6:
        raise ValueError(f"Joints are not of length 6: {joints}")
    for joint in joints:
        if not isinstance(joint, float):
            raise ValueError(f"Joint is not of type float: {joint}")
    return JointState(joints)


def parse_command_message(message: str) -> CommandMessage:
    parsed = json.loads(message)
    if parsed["type"] != MessageType.Command.name:
        raise ValueError(f"Message type: {parsed['type']} is not of type Command {MessageType.Command.name}")
    return CommandMessage(parsed["data"]["id"], parsed["data"]["command"])
