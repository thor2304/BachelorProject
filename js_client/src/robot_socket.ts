function get_socket(ip: string, port: number) {
    return new WebSocket(
        `ws://${ip}:${port}`
    );
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

async function getInterpreterSocket(ip: string) {
    const secondarySocket = get_socket(ip, 30002);

    return new Promise((resolve, reject) => {
        secondarySocket.onopen = () => {
            console.log('secondary socket opened');
            send(secondarySocket, 'interpreter_mode()');
            const interpreterSocket = get_socket(ip, 30020);
            resolve(interpreterSocket);
        };
        secondarySocket.onerror = (event) => {
            reject(event);
        }
    })
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



