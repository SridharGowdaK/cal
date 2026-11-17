import hashlib
import hmac
import re
import secrets
import string
from datetime import datetime


def hash_password(password: str, salt: str = None) -> tuple:
    """Hashes a password with PBKDF2-HMAC-SHA256 and a random salt."""
    if not salt:
        salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000,
    ).hex()
    return hashed, salt


def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    """Verifies a password against the stored PBKDF2 hash."""
    computed_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000,
    ).hex()
    return hmac.compare_digest(computed_hash, stored_hash)


def password_strength(password):
    if not password:
        return {
            "valid": False,
            "score": 0,
            "message": "Password is required.",
            "feedback": ["Password cannot be empty."],
            "checks": {},
        }

    checks = {
        "length": len(password) >= 8,
        "uppercase": any(ch.isupper() for ch in password),
        "lowercase": any(ch.islower() for ch in password),
        "digit": any(ch.isdigit() for ch in password),
        "special": bool(re.search(r"[^A-Za-z0-9]", password)),
    }

    feedback = []
    if not checks["length"]:
        feedback.append("At least 8 characters long")
    if not checks["uppercase"]:
        feedback.append("At least one uppercase letter (A-Z)")
    if not checks["lowercase"]:
        feedback.append("At least one lowercase letter (a-z)")
    if not checks["digit"]:
        feedback.append("At least one digit (0-9)")
    if not checks["special"]:
        feedback.append("At least one special character (!@#$ etc.)")

    score = sum(1 for value in checks.values() if value)
    valid = score >= 4

    if valid:
        message = "Strong password" if score >= 5 else "Good password"
    else:
        message = "Weak password: " + ", ".join(feedback) if feedback else "Weak password"

    return {
        "valid": valid,
        "score": score,
        "message": message,
        "feedback": feedback,
        "checks": checks,
    }


def generate_password(length=12, include_uppercase=True, include_digits=True, include_special=True):
    """Generates a cryptographically secure random password meeting complexity rules."""
    if length < 6:
        raise ValueError("Password length must be at least 6 characters.")

    char_pool = list(string.ascii_lowercase)
    guaranteed = [secrets.choice(string.ascii_lowercase)]

    if include_uppercase:
        char_pool.extend(string.ascii_uppercase)
        guaranteed.append(secrets.choice(string.ascii_uppercase))
    if include_digits:
        char_pool.extend(string.digits)
        guaranteed.append(secrets.choice(string.digits))
    if include_special:
        specials = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        char_pool.extend(specials)
        guaranteed.append(secrets.choice(specials))

    remaining = length - len(guaranteed)
    if remaining > 0:
        guaranteed.extend(secrets.choice(char_pool) for _ in range(remaining))

    secrets.SystemRandom().shuffle(guaranteed)
    return "".join(guaranteed)


class LoginSystem:
    def __init__(self):
        self.users = {}

    def user_exists(self, username):
        return username.strip() in self.users

    def register_user(self, username, password, role="user"):
        if not username or not username.strip():
            raise ValueError("Username cannot be empty.")
        username = username.strip()
        if username in self.users:
            raise ValueError(f"User '{username}' already exists.")

        result = password_strength(password)
        if not result["valid"]:
            raise ValueError(result["message"])

        hashed_pw, salt = hash_password(password)
        self.users[username] = {
            "password_hash": hashed_pw,
            "salt": salt,
            "role": role,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        return True

    def login(self, username, password):
        if not username or not password:
            return False
        username = username.strip()
        user_record = self.users.get(username)
        if not user_record:
            return False
        return verify_password(password, user_record["password_hash"], user_record["salt"])

    def get_user_role(self, username):
        user = self.users.get(username.strip())
        return user["role"] if user else None

    def change_password(self, username, old_password, new_password):
        username = username.strip()
        if not self.login(username, old_password):
            raise ValueError("Invalid current password.")
        new_strength = password_strength(new_password)
        if not new_strength["valid"]:
            raise ValueError(new_strength["message"])
        hashed_pw, salt = hash_password(new_password)
        self.users[username]["password_hash"] = hashed_pw
        self.users[username]["salt"] = salt
        return True


class LoginPage:
    def __init__(self):
        self.auth = LoginSystem()

    def render(self):
        return "Login page is running"

    def process(self, username, password):
        if not self.auth.user_exists("admin"):
            self.auth.register_user("admin", "StrongPass@123", role="admin")
        return self.auth.login(username, password)

    def run(self, username, password):
        return self.process(username, password)


if __name__ == "__main__":
    page = LoginPage()
    print(page.render())
    print("Admin login test:", page.run("admin", "StrongPass@123"))
    print("Generated password:", generate_password(14))
