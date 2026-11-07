import re


def password_strength(password):
    if not password:
        return {"valid": False, "score": 0, "message": "Password is required."}

    checks = {
        "length": len(password) >= 8,
        "uppercase": any(ch.isupper() for ch in password),
        "lowercase": any(ch.islower() for ch in password),
        "digit": any(ch.isdigit() for ch in password),
        "special": bool(re.search(r"[^A-Za-z0-9]", password)),
    }

    score = sum(1 for value in checks.values() if value)
    valid = score >= 4

    if valid:
        message = "Strong password" if score >= 5 else "Good password"
    else:
        message = "Weak password"

    return {
        "valid": valid,
        "score": score,
        "message": message,
        "checks": checks,
    }


class LoginSystem:
    def __init__(self):
        self.users = {}

    def register_user(self, username, password):
        result = password_strength(password)
        if not result["valid"]:
            raise ValueError(result["message"])
        self.users[username] = password
        return True

    def login(self, username, password):
        return self.users.get(username) == password


class LoginPage:
    def __init__(self):
        self.auth = LoginSystem()

    def render(self):
        return "Login page is running"

    def process(self, username, password):
        self.auth.register_user("admin", "StrongPass@123")
        return self.auth.login(username, password)

    def run(self, username, password):
        return self.process(username, password)


if __name__ == "__main__":
    page = LoginPage()
    print(page.render())
    print(page.run("admin", "StrongPass@123"))
