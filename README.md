# Mini App Suite (gitday1)

A feature-rich desktop and CLI productivity application in Python featuring an **Advanced Calculator**, **Secure User Authentication & Management**, and a **Cryptographic Password Generator**, complete with calculation history logging and file export.

---

## 🚀 Key Features

### 1. 🧮 Calculator & Calculation History
* **Basic & Advanced Math**: Supports Addition (`+`), Subtraction (`-`), Multiplication (`*`), Division (`/`), Power / Exponentiation (`^`), Modulo (`%`), and Square Root (`sqrt`).
* **Input Validation & Safety**: Gracefully handles divide-by-zero, negative square roots, and format errors.
* **Timestamped History**: Every calculation records an exact timestamp (`[YYYY-MM-DD HH:MM:SS]`).
* **History Management**: View, count, clear, and export calculation history directly to a `.txt` file.

### 2. 🔐 Security & User Authentication
* **PBKDF2 Hashing with Salt**: Passwords are never stored in plaintext; they are hashed using standard-library `PBKDF2-HMAC-SHA256` with random cryptographic salts.
* **Password Strength Checker**: Multi-factor strength meter scoring 0 to 5 with actionable feedback (length, uppercase, lowercase, numbers, special characters).
* **Separate Registration & Login**: Prevents duplicate username registrations and enforces strong password requirements.
* **Session Management**: Tracks logged-in users and roles (e.g. `admin`, `user`), with instant logout functionality.
* **Password Change**: Allows authenticated users to safely update their passwords.

### 3. 🎲 Password Generator
* **Cryptographically Secure**: Generates random passwords using Python's `secrets` module.
* **Customizable Parameters**: Adjust length (6 to 32 characters) and toggle uppercase letters, digits, and special characters.
* **One-Click Clipboard & Transfer**: Copy to clipboard or transfer directly to the login tab in the GUI.

### 4. 🖥️ Dual Interfaces (GUI & CLI)
* **Tkinter GUI**: Tabbed notebook interface with modern layout, password visibility toggle, real-time feedback, and file dialogs.
* **Interactive CLI**: Menu-driven terminal interface with robust `EOFError` and `ValueError` handling for server or terminal environments.

---

## 📁 Project Structure

```text
gitday1/
│
├── app.py              # Main application entry point (GUI + CLI)
├── calculator.py       # Math logic, operations, and calculation history manager
├── login.py            # Password hashing, validation, generation, and user auth
├── test_features.py    # Comprehensive test suite covering all modules
└── README.md           # Documentation
```

---

## 🛠️ Usage

### Running the Desktop GUI
Ensure Python is installed and run:
```bash
python app.py
```

### Running the CLI Mode
The CLI can be run interactively by calling `app.py` in non-GUI terminal mode, or executing individual modules:
```bash
python -c "import app; app.main()"
```

Default credentials pre-loaded for testing:
* **Username**: `admin`
* **Password**: `StrongPass@123`

---

## 🧪 Running Unit Tests

Run the complete test suite:
```bash
python -m unittest test_features.py -v
```
All tests use Python's built-in `unittest` module with zero external dependencies.
