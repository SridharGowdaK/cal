import tkinter as tk
from tkinter import messagebox, ttk

from calculator import add, subtract, multiply, divide, CalculatorHistory
from login import LoginSystem, password_strength


class AppWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini App")
        self.root.geometry("520x520")
        self.root.resizable(False, False)

        self.history = CalculatorHistory()
        self.auth = LoginSystem()
        self.auth.register_user("admin", "StrongPass@123")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.calculator_tab = ttk.Frame(self.notebook)
        self.login_tab = ttk.Frame(self.notebook)
        self.history_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.calculator_tab, text="Calculator")
        self.notebook.add(self.login_tab, text="Login")
        self.notebook.add(self.history_tab, text="History")

        self.build_calculator_tab()
        self.build_login_tab()
        self.build_history_tab()

    def build_calculator_tab(self):
        tk.Label(self.calculator_tab, text="First number:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.num1_var = tk.StringVar()
        tk.Entry(self.calculator_tab, textvariable=self.num1_var, width=20).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.calculator_tab, text="Second number:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.num2_var = tk.StringVar()
        tk.Entry(self.calculator_tab, textvariable=self.num2_var, width=20).grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.calculator_tab, text="Operation:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.operation_var = tk.StringVar(value="+")
        ttk.Combobox(self.calculator_tab, textvariable=self.operation_var, values=["+", "-", "*", "/"], state="readonly", width=17).grid(row=2, column=1, padx=10, pady=10)

        ttk.Button(self.calculator_tab, text="Calculate", command=self.calculate).grid(row=3, column=0, columnspan=2, pady=10)
        self.result_var = tk.StringVar(value="Result: ")
        tk.Label(self.calculator_tab, textvariable=self.result_var, fg="darkgreen", font=("Arial", 12, "bold")).grid(row=4, column=0, columnspan=2, pady=10)

    def build_login_tab(self):
        tk.Label(self.login_tab, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.username_var = tk.StringVar()
        tk.Entry(self.login_tab, textvariable=self.username_var, width=25).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.login_tab, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.password_var = tk.StringVar()
        tk.Entry(self.login_tab, textvariable=self.password_var, show="*", width=25).grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(self.login_tab, text="Register / Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)
        self.login_status = tk.StringVar(value="")
        tk.Label(self.login_tab, textvariable=self.login_status, fg="blue", wraplength=300, justify="left").grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def build_history_tab(self):
        self.history_box = tk.Listbox(self.history_tab, width=55, height=18)
        self.history_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.refresh_history()

    def calculate(self):
        try:
            first = float(self.num1_var.get())
            second = float(self.num2_var.get())
            operation = self.operation_var.get()

            if operation == "+":
                result = add(first, second)
            elif operation == "-":
                result = subtract(first, second)
            elif operation == "*":
                result = multiply(first, second)
            elif operation == "/":
                result = divide(first, second)
            else:
                raise ValueError("Unsupported operation")

            expression = f"{first} {operation} {second}"
            self.history.add_result(expression, result)
            self.result_var.set(f"Result: {result}")
            self.refresh_history()
        except Exception as exc:
            messagebox.showerror("Calculation error", str(exc))

    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()

        strength = password_strength(password)
        if not strength["valid"]:
            self.login_status.set(f"Password weak: {strength['message']}")
            return

        try:
            self.auth.register_user(username, password)
            if self.auth.login(username, password):
                self.login_status.set(f"Welcome, {username}! Password strength: {strength['score']}/5")
            else:
                self.login_status.set("Login failed.")
        except ValueError as exc:
            self.login_status.set(str(exc))

    def refresh_history(self):
        self.history_box.delete(0, tk.END)
        for entry in self.history.get_history():
            self.history_box.insert(tk.END, entry)


def show_menu():
    print("\n=== Mini App ===")
    print("1. Calculator")
    print("2. Login demo")
    print("3. Exit")


def run_calculator():
    history = CalculatorHistory()
    print("\nCalculator")
    print("Operations: +, -, *, /")
    while True:
        try:
            first = float(input("Enter first number: "))
            second = float(input("Enter second number: "))
            operation = input("Choose operation (+, -, *, /): ").strip()

            if operation == "+":
                result = add(first, second)
            elif operation == "-":
                result = subtract(first, second)
            elif operation == "*":
                result = multiply(first, second)
            elif operation == "/":
                result = divide(first, second)
            else:
                print("Unsupported operation.")
                continue

            expression = f"{first} {operation} {second}"
            history.add_result(expression, result)
            print(f"Result: {result}")
        except ValueError as exc:
            print(f"Invalid input: {exc}")
        except ZeroDivisionError:
            print("You cannot divide by zero.")
        except EOFError:
            print("\nCalculator closed.")
            return

        try:
            again = input("Try again? (y/n): ").strip().lower()
        except EOFError:
            print("\nReturning to menu.")
            return

        if again != "y":
            break


def run_login_demo():
    auth = LoginSystem()
    auth.register_user("admin", "StrongPass@123")
    try:
        username = input("Username: ").strip()
        password = input("Password: ").strip()
    except EOFError:
        print("\nLogin cancelled.")
        return

    strength = password_strength(password)
    if not strength["valid"]:
        print(f"Password is weak: {strength['message']}")
        return

    if auth.login(username, password):
        print(f"Welcome, {username}! Password strength: {strength['score']}/5")
    else:
        print("Invalid username or password.")


def main():
    while True:
        try:
            show_menu()
            choice = input("Choose an option: ").strip()
        except EOFError:
            print("\nExiting app.")
            break

        if choice == "1":
            run_calculator()
        elif choice == "2":
            run_login_demo()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")


if __name__ == "__main__":
    root = tk.Tk()
    app = AppWindow(root)
    root.mainloop()
