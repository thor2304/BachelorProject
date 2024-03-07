import {handleRobotStateMessage} from "./messageHandling/RobotStateMessageHandler";
import {MessageType, RobotStateMessage} from "./messageHandling/messageDefinitions";

const message: RobotStateMessage = {
    type: MessageType.RobotState,
    data: {
        safety_status: 'string',
        runtime_state: 'string',
        robot_mode: 'string',
        joints: [1, 2, 3, 4, 5, 6],
        tcp: {
            pose: [1, 2, 3, 4, 5, 6],
            speed: [1, 2, 3, 4, 5, 6],
            force: [1, 2, 3, 4, 5, 6]
        },
        payload: 1
    }
}

handleRobotStateMessage(message);