
from flask import Flask, jsonify, render_template, request
import json
import urllib.error
import urllib.request

app = Flask(__name__)

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen2.5:1.5b"


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api/health")
def health():
    try:
        req = urllib.request.Request(
            "http://127.0.0.1:11434/api/tags"
        )
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode("utf-8"))

        models = [m["name"] for m in data.get("models", [])]
        return jsonify({
            "status": "ok",
            "ollama": "connected",
            "model_available": any(
                name == MODEL or name.startswith(MODEL + ":")
                for name in models
            ),
            "models": models,
        })
    except (OSError, urllib.error.URLError):
        return jsonify({
            "status": "error",
            "message": "Ollama is not reachable. Start Ollama and retry."
        }), 503


@app.post("/api/mission")
def create_mission():
    body = request.get_json(silent=True) or {}
    minutes = body.get("minutes", 15)
    interest = body.get("interest", "nature")
    difficulty = body.get("difficulty", "beginner")

    if type(minutes) is not int or minutes not in (15, 30, 60):
        return jsonify({"error": "Choose 15, 30, or 60 minutes."}), 400

    allowed_interests = {
        "nature", "walking", "birdwatching", "gardening"
    }
    allowed_difficulties = {"beginner", "easy", "moderate"}

    if interest not in allowed_interests:
        return jsonify({"error": "Choose a listed activity interest."}), 400
    if difficulty not in allowed_difficulties:
        return jsonify({"error": "Choose a listed difficulty."}), 400

    prompt = f"""
Create one practical outdoor mission.
Available time: {minutes} minutes.
Interest: {interest}.
Experience level: {difficulty}.

Return a helpful response with these headings:
Mission, Why it helps, What to do, What to bring, Safety.
Use simple English. Give realistic steps that fit the available time.
Encourage the user to put the phone away after reading.
Do not claim to know the user's location or current weather.
Avoid dangerous, private, or restricted places.
Keep the response under 220 words.
"""

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are TouchGrass AI, a practical outdoor activity "
                    "coach. Help people safely spend time outside. "
                    "Never invent local facts."
                )
            },
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            result = json.loads(response.read().decode("utf-8"))
        mission = result.get("message", {}).get("content", "").strip()

        if not mission:
            return jsonify({"error": "The AI returned an empty response."}), 502

        return jsonify({"mission": mission})

    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return jsonify({
                "error": f"Model {MODEL} was not found. Check `ollama list`."
            }), 503
        return jsonify({"error": f"Ollama returned HTTP {exc.code}."}), 502

    except (OSError, TimeoutError):
        return jsonify({
            "error": "Cannot reach Ollama. Check that Ollama is running."
        }), 503


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
