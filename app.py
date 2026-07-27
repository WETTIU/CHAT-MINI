from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chiave_segretissima_nostra'
socketio = SocketIO(app, cors_allowed_origins="*")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nostra Chat Privata</title>
    <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
    <style>
        body { font-family: sans-serif; background: #ece5dd; margin: 0; padding: 10px; }
        #chat { height: 80vh; overflow-y: scroll; display: flex; flex-direction: column; }
        .msg { background: white; padding: 8px 12px; margin: 5px; border-radius: 8px; max-width: 70%; word-wrap: break-word; }
        .mine { background: #dcf8c6; align-self: flex-end; }
        #input-box { display: flex; position: fixed; bottom: 10px; left: 10px; right: 10px; }
        input { flex: 1; padding: 12px; border: 1px solid #ccc; border-radius: 20px; outline: none; }
        button { padding: 10px 15px; margin-left: 5px; background: #075e54; color: white; border: none; border-radius: 20px; }
    </style>
</head>
<body>
    <div id="chat"></div>
    <div id="input-box">
        <input id="message" placeholder="Scrivi un messaggio..." autocomplete="off"/>
        <button onclick="send()">Invia</button>
    </div>

    <script>
        const socket = io();
        const user = prompt("Come ti chiami?") || "Anonimo";

        socket.on('message', function(data) {
            let div = document.createElement('div');
            div.className = 'msg ' + (data.user === user ? 'mine' : '');
            div.innerHTML = '<b>' + data.user + ':</b> ' + data.msg;
            document.getElementById('chat').appendChild(div);
            window.scrollTo(0, document.body.scrollHeight);
        });

        function send() {
            let input = document.getElementById('message');
            if (input.value.trim() !== '') {
                socket.emit('message', { user: user, msg: input.value });
                input.value = '';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@socketio.on('message')
def handle_message(data):
    emit('message', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)