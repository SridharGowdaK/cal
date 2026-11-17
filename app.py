import threading
import tkinter as tk
import webbrowser
from tkinter import filedialog, messagebox, ttk

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


class AppWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini App Suite + AI")
        self.root.geometry("600x640")
        self.root.resizable(False, False)

        self.history = CalculatorHistory()
        self.auth = LoginSystem()
        self.auth.register_user("admin", "StrongPass@123", role="admin")
        self.current_user = None

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.calculator_tab = ttk.Frame(self.notebook)
        self.login_tab = ttk.Frame(self.notebook)
        self.generator_tab = ttk.Frame(self.notebook)
        self.ai_tab = ttk.Frame(self.notebook)
        self.history_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.calculator_tab, text="Calculator")
        self.notebook.add(self.login_tab, text="User & Auth")
        self.notebook.add(self.generator_tab, text="Password Gen")
        self.notebook.add(self.ai_tab, text="AI Features")
        self.notebook.add(self.history_tab, text="History")

        self.build_calculator_tab()
        self.build_login_tab()
        self.build_generator_tab()
        self.build_ai_tab()
        self.build_history_tab()

    # ------------------ Calculator Tab ------------------
    def build_calculator_tab(self):
        container = ttk.LabelFrame(self.calculator_tab, text=" Calculator Operations ")
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        tk.Label(container, text="First number:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.num1_var = tk.StringVar()
        self.num1_entry = ttk.Entry(container, textvariable=self.num1_var, width=22)
        self.num1_entry.grid(row=0, column=1, padx=10, pady=8)

        tk.Label(container, text="Operation:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=8, sticky="w")
        self.operation_var = tk.StringVar(value="+")
        self.op_combobox = ttk.Combobox(
            container,
            textvariable=self.operation_var,
            values=["+", "-", "*", "/", "^ (power)", "% (modulus)", "sqrt (square root)"],
            state="readonly",
            width=20,
        )
        self.op_combobox.grid(row=1, column=1, padx=10, pady=8)
        self.op_combobox.bind("<<ComboboxSelected>>", self.on_operation_changed)

        tk.Label(container, text="Second number:", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=8, sticky="w")
        self.num2_var = tk.StringVar()
        self.num2_entry = ttk.Entry(container, textvariable=self.num2_var, width=22)
        self.num2_entry.grid(row=2, column=1, padx=10, pady=8)

        btn_frame = ttk.Frame(container)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=12)
        ttk.Button(btn_frame, text="Calculate", command=self.calculate).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_frame, text="Clear Fields", command=self.clear_calculator_fields).pack(side=tk.LEFT, padx=6)

        self.result_var = tk.StringVar(value="Result: --")
        tk.Label(
            container,
            textvariable=self.result_var,
            fg="#1b5e20",
            font=("Arial", 13, "bold"),
        ).grid(row=4, column=0, columnspan=2, pady=10)

    def on_operation_changed(self, event=None):
        op = self.operation_var.get()
        if "sqrt" in op:
            self.num2_entry.config(state="disabled")
            self.num2_var.set("")
        else:
            self.num2_entry.config(state="normal")

    def clear_calculator_fields(self):
        self.num1_var.set("")
        self.num2_var.set("")
        self.result_var.set("Result: --")

    def calculate(self):
        try:
            op_selected = self.operation_var.get().split()[0]
            first_val = self.num1_var.get().strip()
            if not first_val:
                raise ValueError("Please provide the first number.")
            first = float(first_val)

            if op_selected == "sqrt":
                result = square_root(first)
                expression = f"sqrt({first})"
            else:
                second_val = self.num2_var.get().strip()
                if not second_val:
                    raise ValueError(f"Operation '{op_selected}' requires the second number.")
                second = float(second_val)

                if op_selected == "+":
                    result = add(first, second)
                elif op_selected == "-":
                    result = subtract(first, second)
                elif op_selected == "*":
                    result = multiply(first, second)
                elif op_selected == "/":
                    result = divide(first, second)
                elif op_selected == "^":
                    result = power(first, second)
                elif op_selected == "%":
                    result = modulus(first, second)
                else:
                    raise ValueError(f"Unsupported operation: {op_selected}")

                expression = f"{first} {op_selected} {second}"

            self.history.add_result(expression, result)
            self.result_var.set(f"Result: {result}")
            self.refresh_history()
        except Exception as exc:
            messagebox.showerror("Calculation error", str(exc))

    # ------------------ Login & Auth Tab ------------------
    def build_login_tab(self):
        container = ttk.LabelFrame(self.login_tab, text=" User Authentication ")
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        tk.Label(container, text="Username:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.username_var = tk.StringVar()
        ttk.Entry(container, textvariable=self.username_var, width=25).grid(row=0, column=1, padx=10, pady=8)

        tk.Label(container, text="Password:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=8, sticky="w")
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(container, textvariable=self.password_var, show="*", width=25)
        self.password_entry.grid(row=1, column=1, padx=10, pady=8)

        self.show_pw_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            container,
            text="Show Password",
            variable=self.show_pw_var,
            command=self.toggle_password_visibility,
        ).grid(row=2, column=1, sticky="w", padx=10)

        action_frame = ttk.Frame(container)
        action_frame.grid(row=3, column=0, columnspan=2, pady=12)
        ttk.Button(action_frame, text="Log In", command=self.login).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Register New User", command=self.register).pack(side=tk.LEFT, padx=5)

        self.login_status = tk.StringVar(value="")
        tk.Label(
            container,
            textvariable=self.login_status,
            fg="#0d47a1",
            wraplength=380,
            justify="left",
            font=("Arial", 9),
        ).grid(row=4, column=0, columnspan=2, padx=10, pady=8)

        # Active session display
        session_frame = ttk.LabelFrame(container, text=" Active Session ")
        session_frame.grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        self.session_label_var = tk.StringVar(value="Status: Not logged in")
        tk.Label(
            session_frame,
            textvariable=self.session_label_var,
            font=("Arial", 9, "italic"),
            fg="#424242",
        ).pack(side=tk.LEFT, padx=10, pady=8)

        self.logout_btn = ttk.Button(session_frame, text="Logout", command=self.logout, state="disabled")
        self.logout_btn.pack(side=tk.RIGHT, padx=10, pady=5)

    def toggle_password_visibility(self):
        if self.show_pw_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()

        if not username or not password:
            self.login_status.set("Please enter both username and password.")
            return

        if self.auth.login(username, password):
            role = self.auth.get_user_role(username) or "user"
            self.current_user = username
            self.session_label_var.set(f"Logged in as: {username} (Role: {role})")
            self.logout_btn.config(state="normal")
            self.login_status.set(f"Welcome back, {username}!")
            messagebox.showinfo("Login Success", f"Welcome back, {username}!")
        else:
            self.login_status.set("Invalid username or password.")
            messagebox.showwarning("Login Failed", "Invalid username or password.")

    def register(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()

        if not username:
            self.login_status.set("Username cannot be empty.")
            return

        strength = password_strength(password)
        if not strength["valid"]:
            self.login_status.set(f"Password weak: {strength['message']}")
            return

        try:
            self.auth.register_user(username, password)
            self.login_status.set(f"User '{username}' registered successfully! Password score: {strength['score']}/5.")
            messagebox.showinfo("Registration Success", f"User '{username}' registered successfully!")
        except ValueError as exc:
            self.login_status.set(str(exc))
            messagebox.showerror("Registration Error", str(exc))

    def logout(self):
        self.current_user = None
        self.session_label_var.set("Status: Not logged in")
        self.logout_btn.config(state="disabled")
        self.login_status.set("You have been logged out.")

    # ------------------ Password Generator Tab ------------------
    def build_generator_tab(self):
        container = ttk.LabelFrame(self.generator_tab, text=" Secure Password Generator ")
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        tk.Label(container, text="Password Length:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.gen_len_var = tk.IntVar(value=14)
        ttk.Spinbox(container, from_=8, to=32, textvariable=self.gen_len_var, width=10).grid(row=0, column=1, padx=10, pady=8, sticky="w")

        self.gen_upper_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(container, text="Include Uppercase Letters (A-Z)", variable=self.gen_upper_var).grid(row=1, column=0, columnspan=2, padx=10, pady=4, sticky="w")

        self.gen_digits_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(container, text="Include Digits (0-9)", variable=self.gen_digits_var).grid(row=2, column=0, columnspan=2, padx=10, pady=4, sticky="w")

        self.gen_special_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(container, text="Include Special Characters (!@#$)", variable=self.gen_special_var).grid(row=3, column=0, columnspan=2, padx=10, pady=4, sticky="w")

        ttk.Button(container, text="Generate Password", command=self.do_generate_password).grid(row=4, column=0, columnspan=2, pady=12)

        tk.Label(container, text="Generated Password:", font=("Arial", 10)).grid(row=5, column=0, padx=10, pady=6, sticky="w")
        self.generated_pw_var = tk.StringVar()
        self.gen_entry = ttk.Entry(container, textvariable=self.generated_pw_var, width=28, font=("Consolas", 11))
        self.gen_entry.grid(row=5, column=1, padx=10, pady=6, sticky="w")

        btn_row = ttk.Frame(container)
        btn_row.grid(row=6, column=0, columnspan=2, pady=8)
        ttk.Button(btn_row, text="Copy to Clipboard", command=self.copy_generated_password).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_row, text="Use in Login Tab", command=self.use_generated_in_login).pack(side=tk.LEFT, padx=5)

        self.gen_info_var = tk.StringVar(value="")
        tk.Label(container, textvariable=self.gen_info_var, font=("Arial", 9), fg="#2e7d32").grid(row=7, column=0, columnspan=2, padx=10, pady=6)

    def do_generate_password(self):
        try:
            length = self.gen_len_var.get()
            pw = generate_password(
                length=length,
                include_uppercase=self.gen_upper_var.get(),
                include_digits=self.gen_digits_var.get(),
                include_special=self.gen_special_var.get(),
            )
            self.generated_pw_var.set(pw)
            strength = password_strength(pw)
            self.gen_info_var.set(f"Strength: {strength['message']} (Score: {strength['score']}/5)")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def copy_generated_password(self):
        pw = self.generated_pw_var.get()
        if pw:
            self.root.clipboard_clear()
            self.root.clipboard_append(pw)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Notice", "Generate a password first.")

    def use_generated_in_login(self):
        pw = self.generated_pw_var.get()
        if pw:
            self.password_var.set(pw)
            self.notebook.select(self.login_tab)
            messagebox.showinfo("Transferred", "Password set in User & Auth tab.")
        else:
            messagebox.showwarning("Notice", "Generate a password first.")

    # ------------------ History Tab ------------------
    def build_history_tab(self):
        self.history_box = tk.Listbox(self.history_tab, width=58, height=18, font=("Consolas", 9))
        self.history_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        btn_bar = ttk.Frame(self.history_tab)
        btn_bar.pack(pady=8)
        ttk.Button(btn_bar, text="Clear History", command=self.clear_history).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_bar, text="Export to File", command=self.export_history).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_bar, text="Refresh", command=self.refresh_history).pack(side=tk.LEFT, padx=6)

        self.refresh_history()

    # ------------------ AI Tab ------------------
    def build_ai_tab(self):
        container = ttk.LabelFrame(self.ai_tab, text=" AI Math & Security Engine ")
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # AI Math section
        tk.Label(container, text="Natural Language Math Query:", font=("Arial", 9, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=(8, 2), sticky="w")
        self.ai_query_var = tk.StringVar(value="What is 15% of 850?")
        ttk.Entry(container, textvariable=self.ai_query_var, width=38).grid(row=1, column=0, padx=10, pady=4, sticky="w")
        ttk.Button(container, text="Solve with AI", command=self.solve_ai_math).grid(row=1, column=1, padx=6, pady=4)

        self.ai_math_result_var = tk.StringVar(value="Result: --")
        tk.Label(container, textvariable=self.ai_math_result_var, font=("Arial", 10, "bold"), fg="#1b5e20").grid(row=2, column=0, columnspan=2, padx=10, pady=4, sticky="w")

        # AI Security Audit section
        ttk.Separator(container, orient="horizontal").grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)

        tk.Label(container, text="AI Password Security & Entropy Audit:", font=("Arial", 9, "bold")).grid(row=4, column=0, columnspan=2, padx=10, pady=(4, 2), sticky="w")
        self.ai_audit_pw_var = tk.StringVar(value="SecurePass@2026")
        ttk.Entry(container, textvariable=self.ai_audit_pw_var, width=38).grid(row=5, column=0, padx=10, pady=4, sticky="w")
        ttk.Button(container, text="Audit Security", command=self.audit_password_ai).grid(row=5, column=1, padx=6, pady=4)

        self.ai_audit_info_var = tk.StringVar(value="Audit: --")
        tk.Label(container, textvariable=self.ai_audit_info_var, font=("Arial", 9), fg="#0d47a1", justify="left").grid(row=6, column=0, columnspan=2, padx=10, pady=4, sticky="w")

        # Web Frontend Launcher
        ttk.Separator(container, orient="horizontal").grid(row=7, column=0, columnspan=2, sticky="ew", pady=10)
        web_frame = ttk.Frame(container)
        web_frame.grid(row=8, column=0, columnspan=2, pady=10)
        ttk.Button(web_frame, text="🌐 Launch Modern Web Frontend (Browser)", command=self.open_web_frontend).pack(padx=10)

    def solve_ai_math(self):
        query = self.ai_query_var.get().strip()
        if not query:
            return
        solution = solve_natural_language_math(query)
        if solution.get("success"):
            self.ai_math_result_var.set(f"Result: {solution['result']} ({solution.get('interpreted_as')})")
        else:
            self.ai_math_result_var.set(f"Error: {solution.get('error')}")

    def audit_password_ai(self):
        pw = self.ai_audit_pw_var.get()
        if not pw:
            return
        res = audit_password_security(pw)
        if res.get("success"):
            self.ai_audit_info_var.set(
                f"Score: {res['security_score']}/100 | Level: {res['security_level']} | Entropy: {res['entropy_bits']} bits\n"
                f"Est. Crack Time: {res['estimated_crack_time']}"
            )
        else:
            self.ai_audit_info_var.set(f"Error: {res.get('error')}")

    def open_web_frontend(self):
        try:
            import web_app
            threading.Thread(target=lambda: web_app.run_server(port=5000, open_browser=False), daemon=True).start()
        except Exception:
            pass
        webbrowser.open("http://127.0.0.1:5000")
        messagebox.showinfo("Web Frontend", "Web Frontend opened at http://127.0.0.1:5000")

    def clear_history(self):
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear calculation history?"):
            self.history.clear()
            self.refresh_history()

    def export_history(self):
        if self.history.count() == 0:
            messagebox.showwarning("Empty History", "No calculations to export.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Calculation History",
        )
        if filepath:
            try:
                count = self.history.export_to_file(filepath)
                messagebox.showinfo("Export Successful", f"Saved {count} calculation records to {filepath}")
            except Exception as exc:
                messagebox.showerror("Export Error", str(exc))

    def refresh_history(self):
        self.history_box.delete(0, tk.END)
        for entry in self.history.get_history():
            self.history_box.insert(tk.END, entry)


# ==================== CLI Interface ====================
def show_menu():
    print("\n=== Mini App Suite + AI ===")
    print("1. Calculator")
    print("2. Login & User Management")
    print("3. Password Generator")
    print("4. Calculation History")
    print("5. AI Features (Math & Security)")
    print("6. Launch Web Frontend")
    print("7. Exit")


def run_calculator(history_instance=None):
    history = history_instance if history_instance is not None else CalculatorHistory()
    print("\nCalculator")
    print("Operations: +, -, *, /, ^ (power), % (modulus), sqrt (square root)")
    while True:
        try:
            operation = input("Choose operation (+, -, *, /, ^, %, sqrt): ").strip()
            if not operation:
                break

            if operation == "sqrt":
                first = float(input("Enter number: "))
                result = square_root(first)
                expression = f"sqrt({first})"
            else:
                first = float(input("Enter first number: "))
                second = float(input("Enter second number: "))
                if operation == "+":
                    result = add(first, second)
                elif operation == "-":
                    result = subtract(first, second)
                elif operation == "*":
                    result = multiply(first, second)
                elif operation == "/":
                    result = divide(first, second)
                elif operation in ("^", "**"):
                    result = power(first, second)
                elif operation == "%":
                    result = modulus(first, second)
                else:
                    print("Unsupported operation.")
                    continue
                expression = f"{first} {operation} {second}"

            history.add_result(expression, result)
            print(f"Result: {result}")
        except ValueError as exc:
            print(f"Error: {exc}")
        except ZeroDivisionError:
            print("Cannot divide by zero.")
        except EOFError:
            print("\nCalculator closed.")
            return history

        try:
            again = input("Calculate again? (y/n): ").strip().lower()
        except EOFError:
            print("\nReturning to menu.")
            return history

        if again != "y":
            break
    return history


def run_login_demo(auth_instance=None):
    auth = auth_instance if auth_instance is not None else LoginSystem()
    if not auth.user_exists("admin"):
        auth.register_user("admin", "StrongPass@123", role="admin")

    print("\n--- User & Authentication Menu ---")
    print("1. Log in")
    print("2. Register new account")
    print("3. Change password")
    print("4. Check password strength")
    print("5. Back to main menu")

    while True:
        try:
            subchoice = input("Select an option (1-5): ").strip()
        except EOFError:
            print("\nReturning to main menu.")
            return auth

        if subchoice == "1":
            try:
                username = input("Username: ").strip()
                password = input("Password: ").strip()
            except EOFError:
                return auth
            if auth.login(username, password):
                role = auth.get_user_role(username)
                print(f"Login successful! Welcome, {username} (Role: {role}).")
            else:
                print("Login failed: Invalid credentials.")
            break
        elif subchoice == "2":
            try:
                username = input("Enter new username: ").strip()
                password = input("Enter password: ").strip()
            except EOFError:
                return auth
            try:
                auth.register_user(username, password)
                print(f"User '{username}' registered successfully!")
            except ValueError as exc:
                print(f"Registration failed: {exc}")
            break
        elif subchoice == "3":
            try:
                username = input("Username: ").strip()
                old_pw = input("Current password: ").strip()
                new_pw = input("New password: ").strip()
            except EOFError:
                return auth
            try:
                auth.change_password(username, old_pw, new_pw)
                print("Password changed successfully!")
            except ValueError as exc:
                print(f"Error changing password: {exc}")
            break
        elif subchoice == "4":
            try:
                pw = input("Enter password to evaluate: ").strip()
            except EOFError:
                return auth
            analysis = password_strength(pw)
            print(f"Score: {analysis['score']}/5 | Valid: {analysis['valid']}")
            print(f"Message: {analysis['message']}")
            break
        elif subchoice in ("5", "back", "exit"):
            break
        else:
            print("Invalid option. Enter 1-5.")
    return auth


def run_password_generator():
    print("\n--- Password Generator ---")
    try:
        raw_len = input("Password length [default 14]: ").strip()
        length = int(raw_len) if raw_len.isdigit() else 14
        pw = generate_password(length=length)
        print(f"Generated secure password: {pw}")
        analysis = password_strength(pw)
        print(f"Strength score: {analysis['score']}/5 ({analysis['message']})")
    except EOFError:
        print("\nGenerator closed.")
    except Exception as exc:
        print(f"Error: {exc}")


def run_history_demo(history):
    print("\n--- Calculation History ---")
    entries = history.get_history()
    if not entries:
        print("No calculation history found.")
        return

    for idx, entry in enumerate(entries, 1):
        print(f"{idx}. {entry}")

    try:
        action = input("\nOptions: (c)lear history, (e)xport to file, or enter to return: ").strip().lower()
        if action == "c":
            history.clear()
            print("History cleared.")
        elif action == "e":
            path = input("Enter file path to export [default history.txt]: ").strip()
            if not path:
                path = "history.txt"
            count = history.export_to_file(path)
            print(f"Exported {count} records to {path}.")
    except EOFError:
        pass


def run_ai_demo():
    print("\n--- AI Features ---")
    print("1. AI Natural Language Math Solver")
    print("2. AI Password Security & Entropy Audit")
    print("3. AI Assistant Chat")
    print("4. Back to menu")
    while True:
        try:
            choice = input("Select an AI option (1-4): ").strip()
        except EOFError:
            return
        if choice == "1":
            try:
                q = input("Enter math question (e.g. '15% of 850' or 'sqrt of 144 plus 5'): ").strip()
            except EOFError:
                return
            sol = solve_natural_language_math(q)
            if sol.get("success"):
                print(f"Interpreted as: {sol.get('interpreted_as')}")
                print(f"Result: {sol.get('result')}")
                for s in sol.get("steps", []):
                    print(f" - {s}")
            else:
                print(f"Error: {sol.get('error')}")
            break
        elif choice == "2":
            try:
                pw = input("Enter password to audit: ").strip()
            except EOFError:
                return
            audit = audit_password_security(pw)
            if audit.get("success"):
                print(f"Security Score: {audit['security_score']}/100 ({audit['security_level']})")
                print(f"Entropy: {audit['entropy_bits']} bits | Crack Time: {audit['estimated_crack_time']}")
                print("Recommendations:")
                for r in audit.get("recommendations", []):
                    print(f" - {r}")
            break
        elif choice == "3":
            try:
                prompt = input("Ask AI a question: ").strip()
            except EOFError:
                return
            resp = ai_assistant_chat(prompt)
            print(f"\nAI: {resp.get('reply')}\n")
            break
        elif choice in ("4", "back", "exit"):
            break
        else:
            print("Please choose 1-4.")


def main():
    history = CalculatorHistory()
    auth = LoginSystem()
    auth.register_user("admin", "StrongPass@123", role="admin")

    while True:
        try:
            show_menu()
            choice = input("Choose an option: ").strip()
        except EOFError:
            print("\nExiting app.")
            break

        if choice == "1":
            run_calculator(history)
        elif choice == "2":
            run_login_demo(auth)
        elif choice == "3":
            run_password_generator()
        elif choice == "4":
            run_history_demo(history)
        elif choice == "5":
            run_ai_demo()
        elif choice == "6":
            import web_app
            threading.Thread(target=lambda: web_app.run_server(port=5000, open_browser=False), daemon=True).start()
            webbrowser.open("http://127.0.0.1:5000")
            print("Web Frontend started at http://127.0.0.1:5000")
        elif choice in ("7", "exit", "quit"):
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose between 1 and 7.")


if __name__ == "__main__":
    root = tk.Tk()
    app = AppWindow(root)
    root.mainloop()
