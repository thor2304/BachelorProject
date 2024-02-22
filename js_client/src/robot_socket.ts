import {createCommandMessage, parseMessage} from "./messageFactory";
import {MessageType, Status} from "./messages";

function get_socket(ip: string, port: number) {
    const out = new WebSocket(
        `ws://${ip}:${port}`
    );

    out.onmessage = (event) => {
        const response = parseMessage(event.data);
        if (response.type !== MessageType.AckResponse) {
            console.log('not an Ack_response message: ', response);
            return
        }
        const created = document.createElement('p');
        created.textContent = response.data.message;
        created.style.backgroundColor = (response.data.status === 'Ok') ? 'green' : 'red';
        created.style.color = 'black';
        console.log(response);
        document.body.appendChild(created).scrollIntoView({behavior: "smooth"});
    }

    console.log(out)

    return out
}

/**
 *
 * @param socket {WebSocket}
 * @param data {string}
 */
function send(socket: WebSocket, data: string) {
    if (socket.readyState === WebSocket.CLOSED) {
        console.log('socket closed');
        return;
    }
    if (!data.endsWith('\n')) {
        data += '\n';
    }

    const commandMessage = createCommandMessage(1, data);

    console.log('sending command: ' + JSON.stringify(commandMessage));

    socket.send(JSON.stringify(commandMessage));
}

async function testCommands() {
    const proxyServer = get_socket("localhost", 8767);
    proxyServer.onopen = () => {
        console.log('proxy server opened');
        document.addEventListener('commandEntered', function (e: CustomEvent) {
            send(proxyServer, e.detail.text)
        })
    };
}


testCommands().then();



