import {ResponseMessageType} from "../responseMessages/responseMessageDefinitions";
import {CommandMessage, UndoMessage, UserMessageType} from "./userMessageDefinitions";


export function createCommandMessage(id: number, command: string): CommandMessage {
    return {
        type: UserMessageType.Command,
        data: {
            id: id,
            command: command,
        }
    };
}

export function createUndoMessage(id: number): UndoMessage {
    return {
        type: UserMessageType.Undo,
        data: {
            id: id
        }
    };
}