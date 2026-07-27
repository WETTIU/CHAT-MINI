from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chiave_segreta_123'
socketio = SocketIO(app, cors_allowed_origins="*")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nostra Chat</title>
    <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
    <style>
        * { box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background-color: #f0f2f5; margin: 0; padding: 15px; display: flex; flex-direction: column; height: 100vh; }
        h2 { text-align: center; color: #1877f2; margin-top: 0; }
        #chat { flex: 1; overflow-y: auto; background: white; border-radius: 12px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 15px; }
        .msg { background: #e4e6eb; padding: 10px 14px; margin: 6px 0; border-radius: 18px; max-width: 80%; width: fit-content; word-wrap: break-word; }
        .mine { background: #0084ff; color: white; margin-left: auto; }
        #input-container { display: flex; gap: 8px; }
        input { flex: 1; padding: 12px 16px; border: 1px solid #ccc; border-radius: 25px; outline: none; font-size: 16px; }
        button { background: #0084ff; color: white; border: none; padding: 12px 20px; border-radius: 25px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <h2>💬 Chat Privata</h2>
    <div id="chat"></div>
    <div id="input-container">
        <input id="message" placeholder="Scrivi un messaggio..." autocomplete="off"/>
        <button onclick="send()">Invia</button>
    </div>

    <script>
        const socket = io();
        let user = localStorage.getItem('chat_user');
        if (!user) {
            user = prompt("Inserisci il tuo nome:") || "Anonimo";
            localStorage.setItem('chat_user', user);
        }

        socket.on('message', function(data) {
            let div = document.createElement('div');
            div.className = 'msg ' + (data.user === user ? 'mine' : '');
            div.innerHTML = '<b>' + data.user + ':</b> ' + data.msg;
            document.getElementById('chat').appendChild(div);
            let chatBox = document.getElementById('chat');
            chatBox.scrollTop = chatBox.scrollHeight;
        });

        function send() {
            let input = document.getElementById('message');
            if (input.value.trim() !== '') {
                socket.emit('message', { user: user, msg: input.value });
                input.value = '';
            }
        }

        document.getElementById('message').addEventListener("keypress", function(e) {
            if (e.key === "Enter") send();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@socketio.on('message')
def handle_message(data):
    emit('message', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
