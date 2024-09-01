from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from env_var import SECRET_KEY

app = Flask(__name__)
socket = SocketIO(app, cors_allowed_origins="*")
app.config["SECRET_KEY"] = SECRET_KEY
rooms = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create-room", methods=["POST"])
def create_room():
    data = request.json
    room = data["room_name"]
    player1 = data["player_name"]
    
    if data["room_name"] not in rooms:
        rooms[room] = {
            "player1": {"name":None,"sid":None},
            "player2": {"name":None,"sid":None},
            "player1moves":set(),
            "player2moves":set(),
            "len":0,
            "chance":None
        }
        return jsonify({"status":"room_created"})
    else:
        return jsonify({"status":"room_exists"})

@app.route("/join-room", methods=["POST"])
def join_existing_room():
    data = request.json
    room = data["room_name"]
    player = data["player_name"]
    
    if room in rooms:
        for key in ["player1", "player2"]:
            if rooms[room][key]["name"] is None:
                rooms[room][key]["name"] = player
                rooms[room]["len"] += 1
                return render_template("gameroom.html")
        return jsonify({"status": "room_full"})
            
    else:
        return jsonify({"status": "room_not_exist"})


@socket.on("connect")
def handle_connect():
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)