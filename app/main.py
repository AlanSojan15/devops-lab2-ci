"""Flask web app exposing the calculator as a small REST API."""

from flask import Flask, jsonify, render_template, request

from app import calculator

app = Flask(__name__)

OPERATIONS = {
    "add": calculator.add,
    "subtract": calculator.subtract,
    "multiply": calculator.multiply,
    "divide": calculator.divide,
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api")
def api_info():
    return jsonify(message="DevOps Lab 2 - CI with GitHub Actions")


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/<operation>")
def calculate(operation):
    if operation not in OPERATIONS:
        return jsonify(error=f"Unknown operation '{operation}'"), 404
    try:
        a = float(request.args["a"])
        b = float(request.args["b"])
    except (KeyError, ValueError):
        return jsonify(error="Query params 'a' and 'b' must be numbers"), 400
    try:
        result = OPERATIONS[operation](a, b)
    except ValueError as exc:
        return jsonify(error=str(exc)), 400
    return jsonify(operation=operation, a=a, b=b, result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
