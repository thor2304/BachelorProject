import {Message, MessageType} from "./messageDefinitions";

export function handleRobotStateMessage(message: Message): void {
    if (message.type !== MessageType.RobotState) {
        console.log('not a Robot_state message: ', message);
        return;
    }

    throw new Error('Robot_state message handler not implemented');
}