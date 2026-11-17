# Mini App Suite + AI (gitday1)

A full-stack desktop, web, and CLI productivity suite featuring an **AI Natural Language Math Solver**, **AI Password Security & Entropy Auditor**, **AI Assistant**, **Advanced Calculator**, **Cryptographic Authentication**, and a **Modern Web Frontend**.

---

## 🚀 Key Features

### 1. 🤖 AI Capabilities (`ai_service.py`)
* **Natural Language Math Solver**: Solves math questions stated in plain English (e.g., *"What is 18% of 2500?"*, *"square root of 144 plus 25"*, *"solve 3*x + 9 = 24"*). Powered by SymPy with step-by-step reasoning.
* **AI Password & Entropy Auditor**: Computes Shannon keyspace entropy in bits, calculates real-world brute-force crack time against modern GPU clusters (10B guesses/sec), detects dictionary/sequential patterns, and outputs tailored recommendations.
* **AI Assistant & Chat**: Answers math, encryption, and calculation queries. Features an offline intelligent engine with optional **Gemini 1.5 Flash API** integration when an API key is provided.

### 2. 🌐 Modern Web Frontend (`web_app.py`, `templates/`, `static/`)
* **Single-Page Application (SPA)**: Built with Flask, Tailwind CSS, and vanilla JS.
* **Full-Featured Web Tabs**:
  * 🧮 Interactive Calculator with instant feedback
  * 🤖 AI Math Solver with live step breakdown cards
  * 🔐 User Registration & Authentication (PBKDF2-HMAC-SHA256)
  * 🛡️ AI Security Audit & Entropy Gauge
  * 🎲 Secure Password Generator with one-click clipboard copy
  * 💬 AI Assistant Chat Interface
  * 📜 Calculation History Manager

### 3. 🧮 Calculator & Calculation History (`calculator.py`)
* **Basic & Advanced Math**: Supports `+`, `-`, `*`, `/`, `^` (power), `%` (modulus), `sqrt` (square root), and `% of` (percentage).
* **Timestamped History**: Formatted records `[YYYY-MM-DD HH:MM:SS] expression = result`.
* **Export & Clear**: Save calculations to `.txt` files or clear in one click.

### 4. 🔐 Security & User Authentication (`login.py`)
* **PBKDF2 Hashing**: Cryptographic password hashing using PBKDF2-HMAC-SHA256 with 100,000 iterations and random per-user salts.
* **Password Strength Checker**: Multi-factor scoring with actionable feedback.
* **Cryptographic Generator**: Secure random generator meeting complex character set requirements.

### 5. 🖥️ Desktop GUI & CLI (`app.py`)
* **Tkinter Desktop GUI**: Native desktop interface with dedicated AI tabs and a one-click launcher for the web frontend.
* **Interactive CLI**: Menu-driven terminal interface with error guards.

---

## 📁 Project Structure

```text
gitday1/
│
├── app.py              # Main desktop GUI (Tkinter) & interactive CLI
├── web_app.py          # Flask backend REST server & web app runner
├── ai_service.py       # AI natural language math solver, auditor & chat
├── calculator.py       # Core calculator operations & history logging
├── login.py            # PBKDF2 hashing, authentication, & password generator
├── templates/
│   └── index.html      # Modern responsive web frontend (Tailwind CSS)
├── static/
│   ├── app.js          # Client-side reactivity and REST API calls
│   └── style.css       # Custom scrollbars, badges, and layout styling
├── test_features.py    # 14 unit tests covering calculator, auth, AI, & web APIs
└── README.md           # Documentation
```

---

## 🛠️ Usage

### 1. Launch the Modern Web Frontend
Run:
```bash
python web_app.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your web browser.

### 2. Launch the Desktop GUI
```bash
python app.py
```

### 3. Run the Interactive CLI Mode
```bash
python -c "import app; app.main()"
```

Default credentials pre-loaded for testing:
* **Username**: `admin`
* **Password**: `StrongPass@123`

---

## 🧪 Running Unit Tests

Run the complete test suite (14 tests):
```bash
python -m unittest test_features.py -v
```
