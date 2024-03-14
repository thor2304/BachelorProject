import {createCommandMessage, createUndoMessage, parseMessage} from "./messageHandling/messageFactory";
import {Message, MessageType} from "./messageHandling/messageDefinitions";
import {handleAckResponseMessage} from "./messageHandling/AckResponseHandler";
import {handleFeedbackMessage} from "./messageHandling/FeedbackMessageHandler";
import {handleRobotStateMessage} from "./messageHandling/RobotStateMessageHandler";
import {EventList} from "./interaction/EventList";

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

function handleMessageFromProxyServer(message: Message) {
    switch (message.type) {
        case MessageType.AckResponse:
            handleAckResponseMessage(message);
            break;
        case MessageType.Feedback:
            handleFeedbackMessage(message);
            break;
        case MessageType.RobotState:
            handleRobotStateMessage(message);
            break;
        case MessageType.CommandFinished:
            console.log('Command finished: ', message);
            break;
        default:
            console.warn('invalid message type: ', message);
    }
}

/**
 *
 * @param socket {WebSocket}
 * @param message {Message}
 */
function send(socket: WebSocket, message: Message) {
    if (socket.readyState === WebSocket.CLOSED) {
        console.log('socket closed');
        return;
    }

    console.log('sending command: ' + JSON.stringify(message));
    socket.send(JSON.stringify(message));
}

async function testCommands() {
    const proxyServer = get_socket("localhost", 8767);
    const rtdeServer = get_socket("localhost", 8001);

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

    rtdeServer.onopen = () => {
        console.log('RTDE socket opened');
    };
}

testCommands().then();

