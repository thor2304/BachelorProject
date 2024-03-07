import {
    AckResponseMessage, CommandFinishedMessage,
    CommandMessage,
    FeedbackMessage,
    Message,
    MessageType,
    RobotStateMessage,
    Status
} from "./messageDefinitions";

export function parseMessage(message: string): Message {
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
        default:
            throw new Error(`Invalid message type: ${parsed.type}`);
    }
}

function parseStatus(status: string): Status {
    if (status !== "Ok" && status !== "Error") {
        throw new Error(`Invalid status: ${status}`);
    }
    return status === "Ok" ? Status.Ok : Status.Error;
}

export function createCommandMessage(id: number, command: string): CommandMessage {
    return {
        type: MessageType.Command,
        data: {
            id: id,
            command: command,
        }
    };
}



function parseAckResponseMessage(message: any): AckResponseMessage {
    if (message.type !== "Ack_response") {
        throw new Error(`Invalid message type: ${message.type}`);
    }
    return {
        type: MessageType.AckResponse,
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
        type: MessageType.Feedback,
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
        type: MessageType.RobotState,
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
        type: MessageType.CommandFinished,
        data: {
            id: noneGuard(message.data.id),
            command: noneGuard(message.data.command),
            variables: noneGuard(message.data.variables)
        }
    };
}