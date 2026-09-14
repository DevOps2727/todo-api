from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage. Resets every time the app restarts.
tasks = []
next_id = 1


@app.route("/tasks", methods=["POST"])
def add_task():
    global next_id
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "title is required"}), 400

    task = {
        "id": next_id,
        "title": data["title"],
        "done": False
    }
    tasks.append(task)
    next_id += 1

    return jsonify(task), 201


@app.route("/tasks", methods=["GET"])
def list_tasks():
    return jsonify(tasks), 200


@app.route("/tasks/<int:task_id>/done", methods=["PATCH"])
def mark_done(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            return jsonify(task), 200

    return jsonify({"error": "task not found"}), 404


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)