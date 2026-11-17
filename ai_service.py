import math
import os
import re
import requests
import sympy as sp


def parse_natural_language_to_math(query: str) -> tuple[str, str]:
    """Translates common natural language math phrases into clean mathematical expressions."""
    cleaned = query.strip().lower()
    cleaned = re.sub(r"^(what is|calculate|solve|find|evaluate|compute|please calculate|tell me)\s+", "", cleaned, flags=re.I)
    cleaned = cleaned.rstrip("?.! ")

    # Handle percentage: "15% of 850" or "15 percent of 850"
    pct_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:%|percent)\s+of\s+(\d+(?:\.\d+)?)", cleaned)
    if pct_match:
        val1, val2 = pct_match.groups()
        expr = f"({val1} * {val2}) / 100"
        return expr, f"Percentage calculation: {val1}% of {val2}"

    # Replace common wording
    replacements = [
        (r"\bsquare root of\s+([a-zA-Z0-9_.]+)", r"sqrt(\1)"),
        (r"\bcube root of\s+([a-zA-Z0-9_.]+)", r"(\1)**(1/3)"),
        (r"\bto the power of\b", "**"),
        (r"\braised to the power of\b", "**"),
        (r"\braised to\b", "**"),
        (r"\bsquared\b", "**2"),
        (r"\bcubed\b", "**3"),
        (r"\bmultiplied by\b", "*"),
        (r"\btimes\b", "*"),
        (r"\bdivided by\b", "/"),
        (r"\bplus\b", "+"),
        (r"\bminus\b", "-"),
        (r"\bmodulo\b", "%"),
        (r"\bmod\b", "%"),
    ]

    for pattern, repl in replacements:
        cleaned = re.sub(pattern, repl, cleaned)

    return cleaned, "Standard expression"


def solve_natural_language_math(query: str) -> dict:
    """Solves natural language math questions or expressions using SymPy and returns step-by-step reasoning."""
    if not query or not query.strip():
        return {
            "success": False,
            "error": "Query cannot be empty.",
            "query": query,
        }

    raw_query = query.strip()
    expr_str, interpretation = parse_natural_language_to_math(raw_query)

    try:
        # Check if it's an equation to solve, e.g., "2*x + 6 = 14"
        if "=" in expr_str and not expr_str.startswith("=="):
            parts = expr_str.split("=")
            if len(parts) == 2:
                lhs = sp.sympify(parts[0].strip())
                rhs = sp.sympify(parts[1].strip())
                equation = sp.Eq(lhs, rhs)
                free_symbols = list(equation.free_symbols)
                if free_symbols:
                    symbol = free_symbols[0]
                    solutions = sp.solve(equation, symbol)
                    return {
                        "success": True,
                        "type": "algebraic_equation",
                        "query": raw_query,
                        "interpreted_as": f"{lhs} = {rhs}",
                        "variable": str(symbol),
                        "solutions": [str(sol) for sol in solutions],
                        "result": ", ".join(str(sol) for sol in solutions),
                        "steps": [
                            f"Identified equation: {lhs} = {rhs}",
                            f"Isolated variable '{symbol}'",
                            f"Solved: {symbol} = {', '.join(str(s) for s in solutions)}",
                        ],
                    }

        # Otherwise evaluate as expression
        parsed_expr = sp.sympify(expr_str)
        # Numerical evaluation if possible
        evaluated = parsed_expr.evalf() if hasattr(parsed_expr, "evalf") else parsed_expr
        
        # If float and close to integer, format nicely
        if isinstance(evaluated, sp.Float):
            val = float(evaluated)
            if val.is_integer():
                result_display = str(int(val))
            else:
                result_display = f"{val:.6g}"
        else:
            result_display = str(evaluated)

        steps = [
            f"Input query: '{raw_query}'",
            f"Mathematical form: {parsed_expr}",
            f"Evaluated result: {result_display}",
        ]

        return {
            "success": True,
            "type": "arithmetic_evaluation",
            "query": raw_query,
            "interpreted_as": str(parsed_expr),
            "result": result_display,
            "steps": steps,
        }
    except Exception as exc:
        return {
            "success": False,
            "error": f"Could not solve expression: {exc}",
            "query": raw_query,
            "interpreted_as": expr_str,
        }


def audit_password_security(password: str) -> dict:
    """Performs an AI security audit on a password including entropy, crack time, and vulnerability patterns."""
    if not password:
        return {
            "success": False,
            "error": "Password cannot be empty.",
        }

    length = len(password)
    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_digits = bool(re.search(r"[0-9]", password))
    has_special = bool(re.search(r"[^A-Za-z0-9]", password))

    pool_size = 0
    if has_lower:
        pool_size += 26
    if has_upper:
        pool_size += 26
    if has_digits:
        pool_size += 10
    if has_special:
        pool_size += 33

    if pool_size == 0:
        pool_size = 1

    # Entropy = length * log2(pool_size)
    entropy = round(length * math.log2(pool_size), 1)

    # Combinations = pool_size ^ length
    combinations = pool_size ** length

    # Assume attacker tries 10 billion guesses/sec (modern GPU cluster)
    guesses_per_sec = 1e10
    seconds_to_crack = combinations / (2 * guesses_per_sec)  # average crack is half the keyspace

    if seconds_to_crack < 1:
        crack_time = "Instant (< 1 second)"
    elif seconds_to_crack < 60:
        crack_time = f"{seconds_to_crack:.1f} seconds"
    elif seconds_to_crack < 3600:
        crack_time = f"{seconds_to_crack / 60:.1f} minutes"
    elif seconds_to_crack < 86400:
        crack_time = f"{seconds_to_crack / 3600:.1f} hours"
    elif seconds_to_crack < 31536000:
        crack_time = f"{seconds_to_crack / 86400:.1f} days"
    elif seconds_to_crack < 3153600000:
        crack_time = f"{seconds_to_crack / 31536000:.1f} years"
    else:
        crack_time = f"{seconds_to_crack / 31536000:.2e} years (Virtually Uncrackable)"

    # Identify vulnerabilities
    vulnerabilities = []
    recommendations = []

    if length < 8:
        vulnerabilities.append("Critical length: under 8 characters.")
        recommendations.append("Increase length to at least 12-16 characters.")
    elif length < 12:
        vulnerabilities.append("Moderate length: between 8 and 11 characters.")
        recommendations.append("Consider lengthening to 14+ characters for high security.")

    common_words = ["password", "admin", "123456", "qwerty", "welcome", "login", "abc123"]
    for word in common_words:
        if word in password.lower():
            vulnerabilities.append(f"Contains common dictionary pattern or sequence: '{word}'.")
            recommendations.append("Avoid standard dictionary words and sequential keyboard patterns.")
            break

    if re.search(r"(.)\1{2,}", password):
        vulnerabilities.append("Contains 3 or more repeated identical characters in a row.")
        recommendations.append("Remove repeated consecutive characters.")

    if not has_special:
        recommendations.append("Add special symbols (!@#$%^&*) to expand search complexity.")
    if not has_upper:
        recommendations.append("Mix in uppercase letters.")
    if not has_digits:
        recommendations.append("Mix in numerical digits.")

    # Calculate overall security score (0 - 100)
    score = min(100, int(entropy * 1.15))
    if vulnerabilities:
        score = max(5, score - len(vulnerabilities) * 15)

    if score >= 80:
        level = "Very Strong"
        badge_color = "emerald"
    elif score >= 60:
        level = "Strong"
        badge_color = "blue"
    elif score >= 40:
        level = "Moderate"
        badge_color = "amber"
    else:
        level = "Weak / Vulnerable"
        badge_color = "red"

    return {
        "success": True,
        "password_length": length,
        "entropy_bits": entropy,
        "estimated_crack_time": crack_time,
        "security_score": score,
        "security_level": level,
        "badge_color": badge_color,
        "vulnerabilities": vulnerabilities if vulnerabilities else ["No common pattern vulnerabilities detected."],
        "recommendations": recommendations if recommendations else ["Password complies with advanced security best practices!"],
    }


def ai_assistant_chat(prompt: str, api_key: str = None) -> dict:
    """AI Assistant combining local mathematical/security intelligence with optional Gemini API integration."""
    if not prompt or not prompt.strip():
        return {"success": False, "reply": "Please enter a question or prompt."}

    user_text = prompt.strip()
    key = api_key or os.environ.get("GEMINI_API_KEY")

    # If Gemini API key is available, attempt remote query
    if key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": (
                                    "You are an intelligent mathematical and security AI assistant inside Mini App Suite. "
                                    "Provide clear, concise, and helpful answers.\n\n"
                                    f"User: {user_text}"
                                )
                            }
                        ]
                    }
                ]
            }
            res = requests.post(url, json=payload, timeout=8)
            if res.status_code == 200:
                data = res.json()
                reply = data["candidates"][0]["content"]["parts"][0]["text"]
                return {
                    "success": True,
                    "reply": reply,
                    "provider": "Gemini 1.5 Flash",
                }
        except Exception:
            # Fall back to offline AI engine
            pass

    # Built-in offline AI reasoning engine
    lowered = user_text.lower()

    # Math or calculation query
    math_keywords = ["calculate", "solve", "what is", "sqrt", "+", "-", "*", "/", "^", "%", "power of", "percent"]
    if any(k in lowered for k in math_keywords) and any(ch.isdigit() for ch in user_text):
        math_res = solve_natural_language_math(user_text)
        if math_res.get("success"):
            reply = (
                f"### AI Math Solution\n"
                f"**Interpreted as:** `{math_res.get('interpreted_as')}`\n"
                f"**Result:** **`{math_res.get('result')}`**\n\n"
                f"**Steps:**\n" + "\n".join(f"- {s}" for s in math_res.get("steps", []))
            )
            return {"success": True, "reply": reply, "provider": "Local SymPy AI Engine"}

    # Security or password query
    if "password" in lowered or "entropy" in lowered or "security" in lowered or "hash" in lowered:
        if "pbkdf2" in lowered:
            reply = (
                "**PBKDF2 (Password-Based Key Derivation Function 2)** applies a pseudorandom function "
                "(such as HMAC-SHA256) along with a cryptographic salt to the password many thousands of times. "
                "This key stretching makes brute-force dictionary attacks computationally prohibitive."
            )
        elif "entropy" in lowered:
            reply = (
                "**Password Entropy** measures the unpredictability of a password in bits: $E = L \\times \\log_2(N)$, "
                "where $L$ is length and $N$ is pool size. Passwords above 60 bits resist ordinary cracking; "
                "passwords above 80 bits resist supercomputers."
            )
        else:
            reply = (
                "For optimal security, use 14+ characters combining uppercase, lowercase, numbers, and symbols. "
                "Avoid common dictionary words, names, or keyboard patterns. You can use our built-in Password Generator tab!"
            )
        return {"success": True, "reply": reply, "provider": "Local AI Knowledge Base"}

    # General assistance
    return {
        "success": True,
        "reply": (
            f"Hello! I am your **Mini App Suite AI Assistant**. I can help you:\n"
            f"- Solve natural language math equations (e.g., *'18% of 2500'* or *'solve 3x + 9 = 24'*)\n"
            f"- Audit password security and calculate entropy\n"
            f"- Answer technical questions about encryption and mathematics\n\n"
            f"Try asking: *'What is the square root of 256 plus 44?'* or *'Audit password: Str0ngP@ss2026'*."
        ),
        "provider": "Local AI Assistant",
    }
