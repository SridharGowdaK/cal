from calculator import add, subtract, multiply, divide
from login import LoginSystem


def show_menu():
    print("\n=== Mini App ===")
    print("1. Calculator")
    print("2. Login demo")
    print("3. Exit")


def run_calculator():
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

            print(f"Result: {result}")
        except ValueError as exc:
            print(f"Invalid input: {exc}")
        except ZeroDivisionError:
            print("You cannot divide by zero.")

        again = input("Try again? (y/n): ").strip().lower()
        if again != "y":
            break


def run_login_demo():
    auth = LoginSystem()
    auth.register_user("admin", "admin123")

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if auth.login(username, password):
        print(f"Welcome, {username}!")
    else:
        print("Invalid username or password.")


def main():
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

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
    main()
