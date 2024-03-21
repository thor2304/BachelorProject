import json
from builtins import list
from enum import Enum, auto

from rtde.serialize import DataObject


class MessageType(Enum):
    Command = auto()
    Undo = auto()
    Ack_response = auto()
    Feedback = auto()
    Robot_state = auto()
    Undo_response = auto()


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
            raise ValueError(f"Unknown status message: '{message}'")


class UndoStatus(Enum):
    Success = auto()
    Error = auto()
    CommandDidNotExist = auto()
    CommandAlreadyUndone = auto()


class CommandMessageData:
    def __init__(self, id: int, command: str):
        self.id = id
        self.command = command


class UndoMessageData:
    def __init__(self, id: int):
        self.id = id


class UndoResponseMessageData:
    def __init__(self, id: int, status: UndoStatus):
        self.id = id
        self.status = status


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


class CommandMessage:
    def __init__(self, id: int, command: str):
        self.type = MessageType.Command
        self.data: CommandMessageData = CommandMessageData(id, command)

    def get_id(self):
        return self.data.id

    def __str__(self):
        return json.dumps({
            "type": self.type.name,
            "data": {
                "id": self.data.id,
                "command": self.data.command
            }
        })

    def __repr__(self):
        return self.__str__()


class UndoMessage:
    def __init__(self, id: int):
        self.type = MessageType.Undo
        self.data: UndoMessageData = UndoMessageData(id)

    def __str__(self):
        return json.dumps({
            "type": self.type.name,
            "data": {
                "id": self.data.id
            }
        })


class UndoResponseMessage:
    def __init__(self, id: int, status: UndoStatus):
        self.type = MessageType.Undo_response
        self.data: UndoResponseMessageData = UndoResponseMessageData(id, status)

    def __str__(self):
        return json.dumps({
            "type": self.type.name,
            "data": {
                "id": self.data.id,
                "status": self.data.status.name
            }
        })


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

    def dump(self):
        return [self.base, self.shoulder, self.elbow, self.wrist1, self.wrist2, self.wrist3]


class TCPPoseState:
    def __init__(self, pose: list[float, float, float, float, float, float]):
        self.x = pose[0]
        self.y = pose[1]
        self.z = pose[2]
        self.rx = pose[3]
        self.ry = pose[4]
        self.rz = pose[5]

    def __getitem__(self, item) -> float:
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.z
        elif item == 3:
            return self.rx
        elif item == 4:
            return self.ry
        elif item == 5:
            return self.rz
        else:
            raise ValueError(f"Unknown TCP index: {item}")

    def dump(self):
        return [self.x, self.y, self.z, self.rx, self.ry, self.rz]


class TCPSpeedState:
    def __init__(self, speed: list[float, float, float, float, float, float]):
        self.x = speed[0]
        self.y = speed[1]
        self.z = speed[2]
        self.rx = speed[3]
        self.ry = speed[4]
        self.rz = speed[5]

    def __getitem__(self, item) -> float:
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.z
        elif item == 3:
            return self.rx
        elif item == 4:
            return self.ry
        elif item == 5:
            return self.rz
        else:
            raise ValueError(f"Unknown TCP index: {item}")

    def dump(self):
        return [self.x, self.y, self.z, self.rx, self.ry, self.rz]


class TCPForceState:
    def __init__(self, force: list[float, float, float, float, float, float]):
        self.fx = force[0]
        self.fy = force[1]
        self.fz = force[2]
        self.tx = force[3]
        self.ty = force[4]
        self.tz = force[5]

    def __getitem__(self, item) -> float:
        if item == 0:
            return self.fx
        elif item == 1:
            return self.fy
        elif item == 2:
            return self.fz
        elif item == 3:
            return self.tx
        elif item == 4:
            return self.ty
        elif item == 5:
            return self.tz
        else:
            raise ValueError(f"Unknown TCP index: {item}")

    def dump(self):
        return [self.fx, self.fy, self.fz, self.tx, self.ty, self.tz]


class TCPState:
    def __init__(self, pose: TCPPoseState, speed: TCPSpeedState, force: TCPForceState):
        self.pose: TCPPoseState = pose
        self.speed: TCPSpeedState = speed
        self.force: TCPForceState = force

    def dump(self):
        return {
            "pose": self.pose.dump(),
            "speed": self.speed.dump(),
            "force": self.force.dump()
        }


class SafetyStatusTypes(Enum):
    normal_mode = 1
    reduced_mode = 2
    protective_stop = 3
    recovery_mode = 4
    safeguard_stop = 5
    system_emergency_stop = 6
    robot_emergency_stop = 7
    violation = 8
    fault = 9
    validate_joint_id = 10
    undefined_safety_mode = 11
    automatic_mode_safeguard_stop = 12
    system_three_position_enabling_stop = 13


lookup_state_types: dict[int, SafetyStatusTypes] = {element.value: element for element in SafetyStatusTypes}


class RuntimeStateTypes(Enum):
    stopping = 0
    stopped = 1
    playing = 2
    pausing = 3
    paused = 4
    resuming = 5


lookup_runtime_state_types: dict[int, RuntimeStateTypes] = {element.value: element for element in RuntimeStateTypes}


class RobotModeTypes(Enum):
    no_controller = -1
    disconnected = 0
    confirm_safety = 1
    booting = 2
    power_off = 3
    power_on = 4
    idle = 5
    backdrive = 6
    running = 7
    updating_firmware = 8


lookup_robot_mode_types: dict[int, RobotModeTypes] = {element.value: element for element in RobotModeTypes}


class RobotStateData:
    def __init__(self, safety_status: SafetyStatusTypes, runtime_state: RuntimeStateTypes, robot_mode: RobotModeTypes,
                 joints: JointState, tcp: TCPState, payload: float):
        self.safety_status: SafetyStatusTypes = safety_status
        self.runtime_state: RuntimeStateTypes = runtime_state
        self.robot_mode: RobotModeTypes = robot_mode
        self.joints: JointState = joints
        self.tcp: TCPState = tcp
        self.payload: float = payload

    def dump(self):
        """Dumps the data to a dictionary that can be converted to JSON."""
        return {
            "safety_status": self.safety_status.name,
            "runtime_state": self.runtime_state.name,
            "robot_mode": self.robot_mode.name,
            "joints": self.joints.dump(),
            "tcp": self.tcp.dump(),
            "payload": self.payload
        }


class TransmittedInformationOptions(Enum):
    state = "safety_status"
    runtime_state = "runtime_state"
    robot_mode = "robot_mode"
    joints = "actual_q"
    tcp_pose = "actual_TCP_pose"
    tcp_speed = "actual_TCP_speed"
    tcp_force = "actual_TCP_force"
    payload = "payload"


class RobotState:
    def __init__(self, state: DataObject):
        self.type = MessageType.Robot_state
        status: SafetyStatusTypes = ensure_type_of_status(
            state.__getattribute__(TransmittedInformationOptions.state.value))
        runtime_state: RuntimeStateTypes = ensure_type_of_runtime_status(
            state.__getattribute__(TransmittedInformationOptions.runtime_state.value))
        robot_mode: RobotModeTypes = ensure_type_of_robot_mode(
            state.__getattribute__(TransmittedInformationOptions.robot_mode.value))
        joints: JointState = ensure_type_of_joints(state.__getattribute__(TransmittedInformationOptions.joints.value))
        tcp: TCPState = ensure_type_of_tcp(state.__getattribute__(TransmittedInformationOptions.tcp_pose.value),
                                           state.__getattribute__(TransmittedInformationOptions.tcp_speed.value),
                                           state.__getattribute__(TransmittedInformationOptions.tcp_force.value))
        payload: float = ensure_type_of_payload(state.__getattribute__(TransmittedInformationOptions.payload.value))
        self.data: RobotStateData = RobotStateData(status, runtime_state, robot_mode, joints, tcp, payload)

    def __str__(self):
        return json.dumps({
            "type": self.type.name,
            "data": self.data.dump()
        })


def ensure_type_of_status(status: any) -> SafetyStatusTypes:
    if not isinstance(status, int):
        raise ValueError(f"Status is not of type int: {status}")
    if status not in lookup_state_types:
        raise ValueError(f"Status is not a known state: {status}")
    return lookup_state_types[status]


def ensure_type_of_runtime_status(runtime_status: any) -> RuntimeStateTypes:
    if not isinstance(runtime_status, int):
        raise ValueError(f"Runtime status is not of type int: {runtime_status}")
    if runtime_status not in lookup_runtime_state_types:
        raise ValueError(f"Runtime status is not a known state: {runtime_status}")
    return lookup_runtime_state_types[runtime_status]


def ensure_type_of_robot_mode(robot_mode: any) -> RobotModeTypes:
    if not isinstance(robot_mode, int):
        raise ValueError(f"Robot mode is not of type int: {robot_mode}")
    if robot_mode not in lookup_robot_mode_types:
        raise ValueError(f"Robot mode is not a known state: {robot_mode}")
    return lookup_robot_mode_types[robot_mode]


def ensure_type_of_joints(joints: any) -> JointState:
    if not isinstance(joints, list):
        raise ValueError(f"Joints are not of type list: {joints}")
    if len(joints) != 6:
        raise ValueError(f"Joints are not of length 6: {joints}")
    for joint in joints:
        if not isinstance(joint, float):
            raise ValueError(f"Joint is not of type float: {joint}")
    return JointState(joints)


def ensure_type_of_tcp_pose(tcp_pose: any) -> TCPPoseState:
    if not isinstance(tcp_pose, list):
        raise ValueError(f"TCP is not of type list: {tcp_pose}")
    if len(tcp_pose) != 6:
        raise ValueError(f"TCP is not of length 6: {tcp_pose}")
    for tcp_value in tcp_pose:
        if not isinstance(tcp_value, float):
            raise ValueError(f"TCP value is not of type float: {tcp_value}")
    return TCPPoseState(tcp_pose)


def ensure_type_of_tcp_speed(tcp_speed: any) -> TCPSpeedState:
    if not isinstance(tcp_speed, list):
        raise ValueError(f"TCP speed is not of type list: {tcp_speed}")
    if len(tcp_speed) != 6:
        raise ValueError(f"TCP speed is not of length 6: {tcp_speed}")
    for tcp_value in tcp_speed:
        if not isinstance(tcp_value, float):
            raise ValueError(f"TCP speed value is not of type float: {tcp_value}")
    return TCPSpeedState(tcp_speed)


def ensure_type_of_tcp_force(tcp_force: any) -> TCPForceState:
    if not isinstance(tcp_force, list):
        raise ValueError(f"TCP force is not of type list: {tcp_force}")
    if len(tcp_force) != 6:
        raise ValueError(f"TCP force is not of length 6: {tcp_force}")
    for tcp_value in tcp_force:
        if not isinstance(tcp_value, float):
            raise ValueError(f"TCP force value is not of type float: {tcp_value}")
    return TCPForceState(tcp_force)


def ensure_type_of_tcp(tcp_pose: any, tcp_speed: any, tcp_force: any) -> TCPState:
    return TCPState(ensure_type_of_tcp_pose(tcp_pose), ensure_type_of_tcp_speed(tcp_speed),
                    ensure_type_of_tcp_force(tcp_force))


def ensure_type_of_payload(payload: any) -> float:
    if not isinstance(payload, float):
        raise ValueError(f"Payload is not of type float: {payload}")
    return payload


def parse_message(message: str) -> CommandMessage | UndoMessage:
    parsed = json.loads(message)
    # print(f"parsed: {parsed}")

    match parsed:
        case {
            'type': MessageType.Command.name,
            'data': {
                'id': id,
                'command': command
            }
        }:
            return CommandMessage(id, command)
        case {
            'type': MessageType.Undo.name,
            'data': {
                'id': id
            }
        }:
            return UndoMessage(id)
        case _:
            raise ValueError(f"Unknown message structure: {parsed}")
