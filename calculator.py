import math
from datetime import datetime


class CalculatorHistory:
    def __init__(self):
        self.entries = []

    def add_result(self, expression, result):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.entries.append(f"[{now}] {expression} = {result}")

    def get_history(self):
        return list(self.entries)

    def clear(self):
        self.entries.clear()

    def count(self):
        return len(self.entries)

    def export_to_file(self, filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            for entry in self.entries:
                f.write(entry + "\n")
        return len(self.entries)


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def power(a, b):
    return a ** b


def modulus(a, b):
    if b == 0:
        raise ValueError("Cannot modulo by zero")
    return a % b


def square_root(a):
    if a < 0:
        raise ValueError("Cannot calculate square root of a negative number")
    return math.sqrt(a)


def percentage(a, b):
    return (a * b) / 100.0


def calculate(operation, a, b=None):
    binary_operations = {
        "+": add,
        "-": subtract,
        "*": multiply,
        "/": divide,
        "^": power,
        "**": power,
        "%": modulus,
        "percentage": percentage,
    }
    unary_operations = {
        "sqrt": square_root,
    }

    if operation in unary_operations:
        return unary_operations[operation](a)

    if operation in binary_operations:
        if b is None:
            raise ValueError(f"Operation '{operation}' requires a second number.")
        return binary_operations[operation](a, b)

    raise ValueError(f"Unsupported operation: {operation}")


if __name__ == "__main__":
    print("Calculator ready.")
    print("10 + 20 =", add(10, 20))
    print("2 ^ 8 =", power(2, 8))
    print("sqrt(49) =", square_root(49))
