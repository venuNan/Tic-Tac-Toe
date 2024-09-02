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
    if not room:
        return jsonify({"status":"missing-fields"})
    
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
    if not (room and player):
        return jsonify({"status":"missing-fields"})
    if room in rooms:
        if rooms[room]["player1"]["name"] is None:
            rooms[room]["player1"]["name"] = player
            return jsonify({"status":"success","player_num":"1"})
        elif rooms[room]["player2"]["name"] is None:
            rooms[room]["player2"]["name"] = player
            return jsonify({"status":"success","player_num":"2"})
        else:
            return jsonify({"status": "room_full"})
    else:
        return jsonify({"status": "room_not_exist"})

@app.route("/gameroom")
def gameroom():
    room = request.args.get("roomname","")
    playername = request.args.get("playername","")
    player_num = request.args.get("player_num","")
    print("player_num",player_num)
    print("room:",room)
    print("playername:",playername)
    return render_template("gameroom.html",data={"room_name":room,"player_name":playername, "player_num":player_num})

@socket.on("connect")
def handle_connect():
    print("connected")
    room = request.args.get("roomname","")
    playername = request.args.get("playername","")
    playernum = request.args.get("playernum","")
    ssid = request.sid
    try:
        if playernum=="1" and rooms[room]["len"] < 2:
            rooms[room]["player1"]["sid"] = ssid
            rooms[room]["len"] += 1
        elif playernum=="2" and rooms[room]["len"] < 2 :
            rooms[room]["player2"]["sid"] = ssid
            rooms[room]["len"] += 1
        print(rooms[room]["len"])
        if rooms[room]["len"] == 2:
            emit("other_player_name",{"player_name":rooms[room]["player1"]["name"]},to=rooms[room]["player2"]["sid"])
            emit("other_player_name",{"player_name":rooms[room]["player2"]["name"]},to=rooms[room]["player1"]["sid"])
            
            emit

    except Exception as e:
        return jsonify({"status":"error occured"})





if __name__ == "__main__":
    socket.run(app, host="0.0.0.0", port=5000)
