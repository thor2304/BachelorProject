import {
    AckResponseMessage, CommandFinishedMessage,
    FeedbackMessage,
    ResponseMessage,
    ResponseMessageType,
    RobotStateMessage,
    Status, UndoResponseMessage, UndoStatus
} from "./responseMessageDefinitions";

export function parseMessage(message: string): ResponseMessage {
    console.log("Parsing message: ", message)
    const parsed = JSON.parse(message);

    switch (parsed.type) {
        case "Ack_response":
            return parseAckResponseMessage(parsed);
        case "Feedback":
            return parseFeedbackMessage(parsed);
        case "Robot_state":
            return parseRobotStateMessage(parsed);
        case "Command_finished":
            return parseCommandFinishedMessage(parsed);
        case "Undo_response":
            return parseUndoResponseMessage(parsed);
        default:
            throw new Error(`Invalid message type: ${parsed.type}`);
    }
}

function parseStatus(status: string): Status {
    if (!(status in Status)) {
        throw new Error(`Invalid status: ${status}`);
    }
    return status === "Ok" ? Status.Ok : Status.Error;
}

function parseUndoStatus(status: string): UndoStatus {
    if (!(status in UndoStatus)) {
        throw new Error(`Invalid undo status: ${status}`);
    }
    return status as UndoStatus;
}

function parseAckResponseMessage(message: any): AckResponseMessage {
    if (message.type !== "Ack_response") {
        throw new Error(`Invalid message type: ${message.type}`);
    }
    return {
        type: ResponseMessageType.AckResponse,
        data: {
            id: noneGuard(message.data.id),
            status: parseStatus(message.data.status),
            command: noneGuard(message.data.command),
            message: noneGuard(message.data.message)
        }
    };
}

function parseFeedbackMessage(message: any): FeedbackMessage {
    if (message.type !== "Feedback") {
        throw new Error(`Invalid message type: ${message.type}`);
    }
    return {
        type: ResponseMessageType.Feedback,
        data: {
            id: noneGuard(message.data.id),
            message: noneGuard(message.data.message)
        }
    };
}

function noneGuard(value: any): any {
    if (value === null || value === undefined) {
        throw new Error("Unexpected null or undefined value");
    }
    return value;
}

function parseRobotStateMessage(message: any): RobotStateMessage {
    if (message.type !== "Robot_state") {
        throw new Error(`Invalid message type: ${message.type}`);
    }
    return {
        type: ResponseMessageType.RobotState,
        data: {
            safety_status: noneGuard(message.data.safety_status),
            runtime_state: noneGuard(message.data.runtime_state),
            robot_mode: noneGuard(message.data.robot_mode),
            joints: noneGuard(message.data.joints),
            tcp: {
                pose: noneGuard(message.data.tcp.pose),
                speed: noneGuard(message.data.tcp.speed),
                force: noneGuard(message.data.tcp.force)
            },
            payload: noneGuard(message.data.payload)
        }
    };
}

function parseCommandFinishedMessage(message: any): CommandFinishedMessage {
    if (message.type !== "Command_finished") {
        throw new Error(`Invalid message type: ${message.type}`);
    }
    return {
        type: ResponseMessageType.CommandFinished,
        data: {
            id: noneGuard(message.data.id),
            command: noneGuard(message.data.command),
            variables: noneGuard(message.data.variables)
        }
    };
}

function parseUndoResponseMessage(message: any): UndoResponseMessage {
    if (message.type !== "Undo_response") {
        throw new Error(`Invalid message type: ${message.type}`);
    }
    return {
        type: ResponseMessageType.UndoResponse,
        data: {
            id: noneGuard(message.data.id),
            status: parseUndoStatus(message.data.status)
        }
    };
}