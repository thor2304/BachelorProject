import {Message, MessageType} from "./messageDefinitions";

export function handleFeedbackMessage(message: Message): void {
    if (message.type !== MessageType.Feedback) {
        console.log('not a Feedback message: ', message);
        return
    }
    
    throw new Error('Feedback message handler not implemented');
}