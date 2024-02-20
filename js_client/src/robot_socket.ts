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
    // const interpreterSocket = await getInterpreterSocket("localhost");
    //
    // interpreterSocket.onmessage = (event) => {
    //     console.log(event.data);
    // };


    const commands = [
        "movej([0.0, 1.57, 0.0, -1.57, 0.0, 0.0], a=1.4, v=1.05)",
        "set_digital_out(0, True)",
        "set_digital_out(1, False)",
        "set_digital_out(2, True)",
        "set_digital_out(3, True)",
        "popup(\"post\",\"post\")"
    ]

    const proxyServer = get_socket("localhost", 8767);
    proxyServer.onopen = () => {
        console.log('proxy server opened');
        for (const command of commands) {
            send(proxyServer, command);
        }
        document.addEventListener('commandEntered', function (e: CustomEvent) {
            send(proxyServer, e.detail.text)
        })
    };

    // interpreterSocket.onopen = () => {
    //     console.log('interpreter socket opened');
    //     for (const command of commands) {
    //         send(interpreterSocket, command);
    //     }
    // };
}


testCommands().then();



