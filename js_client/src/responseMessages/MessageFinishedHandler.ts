import {ResponseMessage, ResponseMessageType} from "./responseMessageDefinitions";
import {EventList} from "../interaction/EventList";

export function handleCommandFinishedMessage(message: ResponseMessage): void {
    if (message.type !== ResponseMessageType.CommandFinished) {
        console.log('not a Command_finished message: ', message);
        return;
    }

    throw new Error('Command_finished message handler not implemented');
}

export function emitCommandFinishedEvent(message: ResponseMessage): void {
    if (message.type !== ResponseMessageType.CommandFinished) {
        console.warn('not a Command_finished message: ', message,
            "initial implementation will continue to emit event");
    }
    const event = new CustomEvent(EventList.CommandFinished, {
        detail: message
    });
    document.dispatchEvent(event);
}