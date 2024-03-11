import {Message, MessageType} from "./messageDefinitions";

export function handleCommandFinishedMessage(message: Message): void {
    if (message.type !== MessageType.CommandFinished) {
        console.log('not a Command_finished message: ', message);
        return;
    }

    throw new Error('Command_finished message handler not implemented');
}