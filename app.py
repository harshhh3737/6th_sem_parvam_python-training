# app.py
# Live Cricket Sports Score System
# Install Flask first:
# pip install flask

from flask import Flask, request, jsonify, render_template_string
import json
import os

app = Flask(__name__)

FILE_NAME = "matches.json"
TOTAL_OVERS = 20
TOTAL_BALLS = TOTAL_OVERS * 6


# ---------------- FILE FUNCTIONS ---------------- #
def load_match():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            try:
                return json.load(file)
            except:
                return {}
    return {}


def save_match(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


# ---------------- CALCULATIONS ---------------- #
def overs_text(balls):
    overs = balls // 6
    ball = balls % 6
    return f"{overs}.{ball}"


def overs_decimal(balls):
    return (balls // 6) + (balls % 6) / 6


def calculate(match):
    score = match["score"]
    balls = match["balls"]
    target = match["target"]

    played_overs = overs_decimal(balls)

    # Current Run Rate
    if played_overs == 0:
        crr = 0
    else:
        crr = round(score / played_overs, 2)

    # Remaining
    remaining_runs = target - score
    remaining_balls = TOTAL_BALLS - balls

    # Result
    if score >= target:
        status = "Won"
        rrr = 0

    elif remaining_balls == 0:
        status = "Lost"
        rrr = 0

    else:
        status = "In Progress"
        remaining_overs = remaining_balls / 6
        rrr = round(remaining_runs / remaining_overs, 2)

    match["overs"] = overs_text(balls)
    match["crr"] = crr
    match["rrr"] = rrr
    match["status"] = status

    return match


# ---------------- HTML ---------------- #
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Live Cricket Scoreboard</title>
<style>
body{
    font-family:Arial;
    background:#0f172a;
    color:white;
    text-align:center;
}
.container{
    width:500px;
    margin:auto;
    margin-top:30px;
    background:#1e293b;
    padding:20px;
    border-radius:15px;
}
input,button{
    padding:10px;
    margin:5px;
    border:none;
    border-radius:8px;
}
button{
    background:#22c55e;
    color:white;
    cursor:pointer;
}
.score{
    font-size:32px;
    font-weight:bold;
}
</style>
</head>
<body>

<div class="container">
<h2>🏏 Live Cricket Scoreboard</h2>

<input type="text" id="team1" placeholder="Team 1">
<input type="text" id="team2" placeholder="Team 2">
<input type="number" id="target" placeholder="Target Score">
<br>
<button onclick="startMatch()">Start Match</button>

<hr>

<div id="board"></div>

<input type="number" id="runs" placeholder="Runs This Ball">
<button onclick="addBall()">Add Ball</button>

</div>

<script>
function startMatch(){
    fetch('/start',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({
            team1:document.getElementById('team1').value,
            team2:document.getElementById('team2').value,
            target:document.getElementById('target').value
        })
    })
    .then(res=>res.json())
    .then(data=>show(data));
}

function addBall(){
    fetch('/ball',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({
            runs:document.getElementById('runs').value
        })
    })
    .then(res=>res.json())
    .then(data=>{
        show(data);
        document.getElementById('runs').value="";
    });
}

function show(data){
    if(data.error){
        alert(data.error);
        return;
    }

    document.getElementById('board').innerHTML = `
        <h3>${data.team1} vs ${data.team2}</h3>
        <div class="score">${data.score}/${data.wickets}</div>
        <p>Overs: ${data.overs}</p>
        <p>Target: ${data.target}</p>
        <p>CRR: ${data.crr}</p>
        <p>RRR: ${data.rrr}</p>
        <h3>Status: ${data.status}</h3>
    `;
}
</script>

</body>
</html>
"""


# ---------------- ROUTES ---------------- #
@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/start", methods=["POST"])
def start():
    data = request.get_json()

    match = {
        "team1": data["team1"],
        "team2": data["team2"],
        "target": int(data["target"]),
        "score": 0,
        "wickets": 0,
        "balls": 0
    }

    match = calculate(match)
    save_match(match)

    return jsonify(match)


@app.route("/ball", methods=["POST"])
def ball():
    match = load_match()

    if not match:
        return jsonify({"error": "Start match first"})

    if match["status"] != "In Progress":
        return jsonify(match)

    data = request.get_json()
    runs = int(data["runs"])

    match["score"] += runs
    match["balls"] += 1

    match = calculate(match)
    save_match(match)

    return jsonify(match)


# ---------------- MAIN ---------------- #
if __name__ == "__main__":
    app.run(debug=True)