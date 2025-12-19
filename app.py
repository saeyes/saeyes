from flask import Flask, render_template, request, jsonify
import random, string

app = Flask(__name__)

rooms = {}

def make_room():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

one_shot = set(open("one_shot.txt", encoding="utf-8").read().split())

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create", methods=["POST"])
def create():
    room = make_room()
    rooms[room] = {
        "current": "",
        "used": [],
        "turn": 0,
        "players": []
    }
    return jsonify({"room": room})

@app.route("/join", methods=["POST"])
def join():
    room = request.json["room"]
    name = request.json["name"]

    if room not in rooms:
        return jsonify({"error": "방 없음"})

    if name not in rooms[room]["players"]:
        rooms[room]["players"].append(name)

    return jsonify(rooms[room])

@app.route("/state")
def state():
    room = request.args.get("room")
    return jsonify(rooms.get(room, {}))

@app.route("/word", methods=["POST"])
def word():
    room = request.json["room"]
    name = request.json["name"]
    word = request.json["word"]

    game = rooms.get(room)
    if not game:
        return jsonify({"error": "방 없음"})

    if game["players"][game["turn"]] != name:
        return jsonify({"error": "당신 차례 아님"})

    if word in game["used"]:
        return jsonify({"error": "이미 사용한 단어"})

    if game["current"] and game["current"][-1] != word[0]:
        return jsonify({"error": "끝말 규칙 위반"})

    # 🔥 한방금지
    if word[-1] in one_shot:
        return jsonify({"error": "❌ 한방 단어 금지"})

    game["used"].append(word)
    game["current"] = word
    game["turn"] = (game["turn"] + 1) % len(game["players"])

    return jsonify(game)

if __name__ == "__main__":
    app.run(debug=True)
