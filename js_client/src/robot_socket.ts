function get_socket(ip: string, port: number) {
    const out = new WebSocket(
        `ws://${ip}:${port}`
    );

    out.onmessage = (event) => {
        const response = JSON.parse(event.data);



        console.log(response);
    }

    console.log(out)

    return out
}

/**
 *
 * @param socket {WebSocket}
 * @param data {string}
 */
function send(socket: WebSocket, data: any) {
    if (socket.readyState === WebSocket.CLOSED) {
        console.log('socket closed');
        return;
    }
    if (!data.endsWith('\n')) {
        data += '\n';
    }

    console.log('sending command: ' + data)

    socket.send(data);
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



