# gui_server.py
from flask import Flask, send_from_directory, request, redirect, url_for, jsonify
import json
import os

APP_DIR = os.path.dirname(__file__)
app = Flask(__name__, static_folder=APP_DIR, template_folder=APP_DIR)

CMD_FILE = os.path.join(APP_DIR, 'commands.json')

def load_commands():
    if not os.path.exists(CMD_FILE):
        with open(CMD_FILE, 'w') as f:
            json.dump({}, f)
    with open(CMD_FILE, 'r') as f:
        return json.load(f)

def save_commands(cmds):
    with open(CMD_FILE, 'w') as f:
        json.dump(cmds, f, indent=2)

@app.route('/')
def index():
    return send_from_directory('.', 'panel.html')

@app.route('/api/commands', methods=['GET'])
def api_get_commands():
    return jsonify(load_commands())

@app.route('/api/commands', methods=['POST'])
def api_save_command():
    data = request.json
    if not data or 'name' not in data or 'response' not in data:
        return {'error': 'invalid'}, 400
    cmds = load_commands()
    cmds[data['name']] = data['response']
    save_commands(cmds)
    return {'ok': True}

@app.route('/api/commands/<name>', methods=['DELETE'])
def api_delete_command(name):
    cmds = load_commands()
    if name in cmds:
        cmds.pop(name)
        save_commands(cmds)
        return {'ok': True}
    return {'error': 'not found'}, 404

def start_gui():
    # Replit gebruikt vaak PORT in env; default 8080
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
