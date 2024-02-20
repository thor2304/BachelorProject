import {
    AckResponseMessage,
    CommandMessage,
    FeedbackMessage,
    Message,
    MessageType,
    RobotStateMessage,
    Status
} from "./messages";

export function parseMessage(message: string): Message {
    const parsed = JSON.parse(message);

    switch (parsed.type) {
        case "Ack_response":
            return createAckResponseMessage(parsed);
        case "Feedback":
            return createFeedbackMessage(parsed);
        case "Robot_state":
            return createRobotStateMessage(parsed);
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



function createAckResponseMessage(message: any): AckResponseMessage {
    if (message.type !== "Ack_response") {
        throw new Error(`Invalid message type: ${message.type}`);
    }
    return {
        type: MessageType.AckResponse,
        data: {
            id: 1,
            status: parseStatus(message.data.status),
            command: message.data.command,
            message: message.data.message
        }
    };
}

function createFeedbackMessage(message: any): FeedbackMessage {
    if (message.type !== "Feedback") {
        throw new Error(`Invalid message type: ${message.type}`);
    }
    return {
        type: MessageType.Feedback,
        data: {
            id: 1,
            message: message.data.message
        }
    };
}

function createRobotStateMessage(message: any): RobotStateMessage {
    if (message.type !== "Robot_state") {
        throw new Error(`Invalid message type: ${message.type}`);
    }
    return {
        type: MessageType.RobotState,
        data: {
            state: message.data.state,
            joints: message.data.joints
        }
    };
}