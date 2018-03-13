let connection = undefined;

function getConnection() {
    if (connection === undefined) {
        connection = new WebSocket('ws://0.0.0.0:8080/ws');

        connection.onopen = () => {
            console.log('Connection is opened');
        };

        connection.onclose = () => {
            console.log('Connection is closed');
        };

        connection.onerror = error => {
            console.log('Connection is errored. Detail: ' + error);
        };

        connection.onmessage = e => {
            console.log('New message: ' + e.data);
        };
    }
    return connection;
}

function init() {
    getConnection();
}

function sendMessage() {
    const connection = getConnection();
    connection.send('subscribe');
}

const readyStateCheckInterval = setInterval(function() {
    if (document.readyState === "complete") {
        clearInterval(readyStateCheckInterval);
        init();
    }
}, 10);
