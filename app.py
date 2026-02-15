from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/play", methods=["POST"])
def play():
    user_choice = request.json["choice"]
    choices = ["rock", "paper", "scissors"]
    ai_choice = random.choice(choices)

    if user_choice == ai_choice:
        result = "Draw 🤝"
    elif (user_choice == "rock" and ai_choice == "scissors") or \
         (user_choice == "paper" and ai_choice == "rock") or \
         (user_choice == "scissors" and ai_choice == "paper"):
        result = "You Win 🏆"
    else:
        result = "AI Wins 🤖"

    return jsonify({
        "ai": ai_choice,
        "result": result
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
