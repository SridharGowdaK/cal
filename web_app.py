import os
import webbrowser
from flask import Flask, jsonify, render_template, request

from ai_service import (
    ai_assistant_chat,
    audit_password_security,
    solve_natural_language_math,
)
from calculator import (
    CalculatorHistory,
    add,
    calculate as calc_op,
    divide,
    modulus,
    multiply,
    percentage,
    power,
    square_root,
    subtract,
)
from login import (
    LoginSystem,
    generate_password,
    password_strength,
)

app = Flask(__name__, template_folder="templates", static_folder="static")

# Shared state instances
history_store = CalculatorHistory()
auth_store = LoginSystem()
auth_store.register_user("admin", "StrongPass@123", role="admin")


# ---------------- HTML Page ----------------
@app.route("/")
def index():
    return render_template("index.html")


# ---------------- Calculator APIs ----------------
@app.route("/api/calculate", methods=["POST"])
def api_calculate():
    data = request.get_json() or {}
    op = data.get("operation", "+").strip()
    a_val = data.get("a")
    b_val = data.get("b")

    if a_val is None:
        return jsonify({"success": False, "error": "First number ('a') is required."}), 400

    try:
        a = float(a_val)
        if op == "sqrt":
            result = square_root(a)
            expr = f"sqrt({a})"
        else:
            if b_val is None:
                return jsonify({"success": False, "error": f"Operation '{op}' requires second number ('b')."}), 400
            b = float(b_val)
            if op == "+":
                result = add(a, b)
            elif op == "-":
                result = subtract(a, b)
            elif op == "*":
                result = multiply(a, b)
            elif op == "/":
                result = divide(a, b)
            elif op in ("^", "**"):
                result = power(a, b)
            elif op == "%":
                result = modulus(a, b)
            elif op == "percentage":
                result = percentage(a, b)
            else:
                return jsonify({"success": False, "error": f"Unsupported operation: {op}"}), 400
            expr = f"{a} {op} {b}"

        history_store.add_result(expr, result)
        return jsonify({"success": True, "expression": expr, "result": result})
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 400


@app.route("/api/history", methods=["GET"])
def api_get_history():
    return jsonify({"success": True, "history": history_store.get_history(), "count": history_store.count()})


@app.route("/api/history", methods=["DELETE"])
def api_clear_history():
    history_store.clear()
    return jsonify({"success": True, "message": "History cleared."})


# ---------------- Auth APIs ----------------
@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"success": False, "error": "Username and password required."}), 400

    if auth_store.login(username, password):
        role = auth_store.get_user_role(username) or "user"
        return jsonify({"success": True, "message": f"Welcome back, {username}!", "username": username, "role": role})
    return jsonify({"success": False, "error": "Invalid username or password."}), 401


@app.route("/api/register", methods=["POST"])
def api_register():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"success": False, "error": "Username and password required."}), 400

    try:
        auth_store.register_user(username, password)
        role = auth_store.get_user_role(username) or "user"
        return jsonify({"success": True, "message": f"User '{username}' registered successfully!", "username": username, "role": role})
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400


@app.route("/api/password/strength", methods=["POST"])
def api_password_strength():
    data = request.get_json() or {}
    password = data.get("password", "")
    analysis = password_strength(password)
    return jsonify({"success": True, "analysis": analysis})


@app.route("/api/password/generate", methods=["POST"])
def api_password_generate():
    data = request.get_json() or {}
    length = int(data.get("length", 14))
    include_upper = bool(data.get("include_uppercase", True))
    include_digits = bool(data.get("include_digits", True))
    include_special = bool(data.get("include_special", True))

    try:
        pw = generate_password(
            length=length,
            include_uppercase=include_upper,
            include_digits=include_digits,
            include_special=include_special,
        )
        analysis = password_strength(pw)
        return jsonify({"success": True, "password": pw, "analysis": analysis})
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 400


# ---------------- AI APIs ----------------
@app.route("/api/ai/solve-math", methods=["POST"])
def api_ai_solve_math():
    data = request.get_json() or {}
    query = data.get("query", "")
    solution = solve_natural_language_math(query)
    return jsonify(solution)


@app.route("/api/ai/audit-password", methods=["POST"])
def api_ai_audit_password():
    data = request.get_json() or {}
    password = data.get("password", "")
    audit = audit_password_security(password)
    return jsonify(audit)


@app.route("/api/ai/chat", methods=["POST"])
def api_ai_chat():
    data = request.get_json() or {}
    prompt = data.get("prompt", "")
    api_key = data.get("api_key")
    response = ai_assistant_chat(prompt, api_key=api_key)
    return jsonify(response)


def run_server(port=5000, open_browser=False):
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", port))
    if open_browser and os.environ.get("DOCKER_CONTAINER") != "1":
        try:
            webbrowser.open(f"http://127.0.0.1:{port}")
        except Exception:
            pass
    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Mini App Suite Web Frontend at http://0.0.0.0:{port}")
    should_open = os.environ.get("DOCKER_CONTAINER") != "1" and not os.environ.get("NO_BROWSER")
    run_server(port=port, open_browser=should_open)
