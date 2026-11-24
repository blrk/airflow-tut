import json
from flask import Flask, jsonify

app = Flask(__name__)

with open("dummy-user.json", "r", encoding="utf-8") as f:
    USER_DATA = json.load(f)

@app.route("/user", methods=["GET"])
def get_user():
    return jsonify(USER_DATA)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
