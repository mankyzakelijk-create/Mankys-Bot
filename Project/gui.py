from flask import Flask, render_template, request, redirect
import json
import threading

app = Flask(__name__)

def load_commands():
    with open("commands.json", "r") as f:
        return json.load(f)

def save_commands(cmds):
    with open("commands.json", "w") as f:
        json.dump(cmds, f, indent=4)

@app.route("/")
def index():
    cmds = load_commands()
    return render_template("index.html", commands=cmds)

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    response = request.form["response"]

    cmds = load_commands()
    cmds[name] = response
    save_commands(cmds)

    return redirect("/")

def start_gui():
    thread = threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8080))
    thread.start()
