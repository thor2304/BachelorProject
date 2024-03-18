import {ResponseMessage, ResponseMessageType} from "./responseMessageDefinitions";
import {emitCommandFinishedEvent} from "./MessageFinishedHandler";

export function handleRobotStateMessage(message: ResponseMessage): void {
    if (message.type !== ResponseMessageType.RobotState) {
        console.log('not a Robot_state message: ', message);
        return;
    }
    console.log('Robot_state message: ', message);

    // throw new Error('Robot_state message handler not implemented');
}