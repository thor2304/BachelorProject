import {ResponseMessage, ResponseMessageType} from "./responseMessageDefinitions";

export function handleFeedbackMessage(message: ResponseMessage): void {
    if (message.type !== ResponseMessageType.Feedback) {
        console.log('not a Feedback message: ', message);
        return
    }
    
    throw new Error('Feedback message handler not implemented');
}