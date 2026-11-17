import builtins
import os
import tempfile
import unittest
from unittest.mock import patch

from app import main
from calculator import (
    add,
    subtract,
    multiply,
    divide,
    power,
    modulus,
    square_root,
    percentage,
    calculate,
    CalculatorHistory,
)
from login import (
    LoginSystem,
    LoginPage,
    password_strength,
    generate_password,
    hash_password,
    verify_password,
)


class FeatureTests(unittest.TestCase):
    def test_calculator_basic_operations(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(subtract(10, 4), 6)
        self.assertEqual(multiply(3, 4), 12)
        self.assertEqual(divide(8, 2), 4)

    def test_calculator_advanced_operations(self):
        self.assertEqual(power(2, 4), 16)
        self.assertEqual(modulus(14, 4), 2)
        self.assertEqual(square_root(25), 5.0)
        self.assertEqual(percentage(200, 15), 30.0)

        # calculate dispatcher
        self.assertEqual(calculate("+", 5, 5), 10)
        self.assertEqual(calculate("-", 10, 3), 7)
        self.assertEqual(calculate("*", 4, 3), 12)
        self.assertEqual(calculate("/", 9, 3), 3.0)
        self.assertEqual(calculate("^", 3, 2), 9)
        self.assertEqual(calculate("%", 10, 3), 1)
        self.assertEqual(calculate("sqrt", 16), 4.0)

    def test_calculator_edge_cases(self):
        with self.assertRaises(ValueError):
            divide(10, 0)
        with self.assertRaises(ValueError):
            modulus(10, 0)
        with self.assertRaises(ValueError):
            square_root(-4)
        with self.assertRaises(ValueError):
            calculate("unknown_op", 1, 2)
        with self.assertRaises(ValueError):
            calculate("+", 1)  # Missing second operand

    def test_calculator_history_enhanced(self):
        history = CalculatorHistory()
        self.assertEqual(history.count(), 0)

        history.add_result("10 + 5", 15)
        history.add_result("4 * 5", 20)
        self.assertEqual(history.count(), 2)
        self.assertIn("10 + 5 = 15", history.get_history()[0])
        self.assertIn("4 * 5 = 20", history.get_history()[1])

        # Test export to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
            tmp_path = tmp.name

        try:
            exported_count = history.export_to_file(tmp_path)
            self.assertEqual(exported_count, 2)
            with open(tmp_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            self.assertEqual(len(lines), 2)
            self.assertIn("10 + 5 = 15", lines[0])
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

        # Clear history
        history.clear()
        self.assertEqual(history.count(), 0)
        self.assertEqual(len(history.get_history()), 0)

    def test_password_hashing_and_verification(self):
        pw = "MySecretPass#2026"
        hashed, salt = hash_password(pw)
        self.assertTrue(verify_password(pw, hashed, salt))
        self.assertFalse(verify_password("WrongSecret#2026", hashed, salt))

    def test_password_generator(self):
        pw = generate_password(16)
        self.assertEqual(len(pw), 16)
        result = password_strength(pw)
        self.assertTrue(result["valid"])

        with self.assertRaises(ValueError):
            generate_password(4)

    def test_login_system(self):
        auth = LoginSystem()
        auth.register_user("alice", "StrongPass@123", role="admin")
        self.assertTrue(auth.login("alice", "StrongPass@123"))
        self.assertFalse(auth.login("alice", "wrongpass"))
        self.assertEqual(auth.get_user_role("alice"), "admin")

        # Duplicate registration prevented
        with self.assertRaises(ValueError):
            auth.register_user("alice", "AnotherPass@456")

        # Weak password rejected
        with self.assertRaises(ValueError):
            auth.register_user("bob", "weak")

        # Password change
        auth.change_password("alice", "StrongPass@123", "NewStrong@999")
        self.assertTrue(auth.login("alice", "NewStrong@999"))
        self.assertFalse(auth.login("alice", "StrongPass@123"))

    def test_login_page_wrapper(self):
        page = LoginPage()
        self.assertIn("Login page is running", page.render())
        self.assertTrue(page.run("admin", "StrongPass@123"))

    def test_main_handles_eof(self):
        with patch.object(builtins, "input", side_effect=EOFError):
            main()

    def test_password_strength_and_history(self):
        result = password_strength("StrongPass@123")
        self.assertTrue(result["valid"])
        self.assertGreaterEqual(result["score"], 3)

        weak_res = password_strength("abc")
        self.assertFalse(weak_res["valid"])
        self.assertGreater(len(weak_res["feedback"]), 0)

        history = CalculatorHistory()
        history.add_result("10 + 5", 15)
        self.assertIn("10 + 5 = 15", history.get_history()[-1])


if __name__ == "__main__":
    unittest.main()
