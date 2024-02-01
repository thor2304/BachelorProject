function get_socket(ip, port) {
    return new WebSocket(
        `ws://${ip}:${port}`
    );
}

/**
 *
 * @param socket {WebSocket}
 * @param data {string}
 */
function send(socket, data) {
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

async function getInterpreterSocket(ip) {
    const secondarySocket = get_socket(ip, 30002);

    const out = new Promise((resolve, reject) => {
        secondarySocket.onopen = () => {
            console.log('secondary socket opened');
            send(secondarySocket, 'interpreter_mode()');
            const interpreterSocket = get_socket(ip, 30020);
            resolve(interpreterSocket);
        };
        secondarySocket.onerror = (event) => {
            reject(event);
        }
    });

    return out
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

    const proxyServer = get_socket("localhost", 8765);
    proxyServer.onopen = () => {
        console.log('proxy server opened');
        for (const command of commands) {
            send(proxyServer, command);
        }
        document.addEventListener('commandEntered', function (e) {
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



