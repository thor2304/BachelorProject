import {createCommandMessage, parseMessage} from "./messageHandling/messageFactory";
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
 * @param data {string}
 * @param id {number}
 */
function send(socket: WebSocket, data: string, id: number) {
    if (socket.readyState === WebSocket.CLOSED) {
        console.log('socket closed');
        return;
    }
    if (!data.endsWith('\n')) {
        data += '\n';
    }

    const commandMessage = createCommandMessage(id, data);

    console.log('sending command: ' + JSON.stringify(commandMessage));

    socket.send(JSON.stringify(commandMessage));
}

async function testCommands() {
    const proxyServer = get_socket("localhost", 8767);
    const rtdeServer = get_socket("localhost", 8001);

    proxyServer.onopen = () => {
        console.log('proxy server opened');
        document.addEventListener(EventList.CommandEntered, function (e: CustomEvent) {
            send(proxyServer, e.detail.text, e.detail.id)
        })
    };

    rtdeServer.onopen = () => {
        console.log('RTDE socket opened');
    };
}

testCommands().then();

