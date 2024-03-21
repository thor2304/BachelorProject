import {parseMessage} from "./responseMessages/responseMessageParsing";
import {ResponseMessage, ResponseMessageType} from "./responseMessages/responseMessageDefinitions";
import {handleAckResponseMessage} from "./responseMessages/AckResponseHandler";
import {handleFeedbackMessage} from "./responseMessages/FeedbackMessageHandler";
import {handleRobotStateMessage} from "./responseMessages/RobotStateMessageHandler";
import {EventList} from "./interaction/EventList";
import {createCommandMessage, createUndoMessage} from "./userMessages/userMessageFactory";
import {UserMessage} from "./userMessages/userMessageDefinitions";
import {handleCommandFinishedMessage} from "./responseMessages/MessageFinishedHandler";

function get_socket(ip: string, port: number) {
    const out = new WebSocket(
        `ws://${ip}:${port}`
    );

    out.onmessage = (event) => {
        const response = parseMessage(event.data);
        handleMessageFromProxyServer(response);
    }

    console.log(out)

    return out
}

function handleMessageFromProxyServer(message: ResponseMessage) {
    switch (message.type) {
        case ResponseMessageType.AckResponse:
            handleAckResponseMessage(message);
            break;
        case ResponseMessageType.Feedback:
            handleFeedbackMessage(message);
            break;
        case ResponseMessageType.RobotState:
            handleRobotStateMessage(message);
            break;
        case ResponseMessageType.CommandFinished:
            handleCommandFinishedMessage(message);
            break;
        case ResponseMessageType.UndoResponse:
            console.log('Undo response: ', message);
            break;
        default:
            console.warn('invalid message type: ', message);
    }
}

/**
 *
 * @param socket {WebSocket}
 * @param message {UserMessage}
 */
function send(socket: WebSocket, message: UserMessage) {
    if (socket.readyState === WebSocket.CLOSED) {
        console.log('socket closed');
        return;
    }

    console.log('sending command: ' + JSON.stringify(message));
    socket.send(JSON.stringify(message));
}

async function testCommands() {
    const proxyServer = get_socket("localhost", 8767);

    proxyServer.onopen = () => {
        console.log('proxy server opened');
        document.addEventListener(EventList.CommandEntered, function (e: CustomEvent) {
            const commandMessage = createCommandMessage(e.detail.id, e.detail.text);
            send(proxyServer, commandMessage)
        });
        document.addEventListener(EventList.UndoEvent, function (e: CustomEvent) {
            const undoCommand = createUndoMessage(e.detail.id);
            send(proxyServer, undoCommand);
        });
    };
}

testCommands().then();

