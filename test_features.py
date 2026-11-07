import builtins
import unittest
from unittest.mock import patch

from app import main
from calculator import add, subtract, multiply, divide, CalculatorHistory
from login import LoginSystem, password_strength


class FeatureTests(unittest.TestCase):
    def test_calculator_basic_operations(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(subtract(10, 4), 6)
        self.assertEqual(multiply(3, 4), 12)
        self.assertEqual(divide(8, 2), 4)

    def test_login_system(self):
        auth = LoginSystem()
        auth.register_user("alice", "StrongPass@123")
        self.assertTrue(auth.login("alice", "StrongPass@123"))
        self.assertFalse(auth.login("alice", "wrongpass"))

    def test_main_handles_eof(self):
        with patch.object(builtins, "input", side_effect=EOFError):
            main()

    def test_password_strength_and_history(self):
        result = password_strength("StrongPass@123")
        self.assertTrue(result["valid"])
        self.assertGreaterEqual(result["score"], 3)

        history = CalculatorHistory()
        history.add_result("10 + 5", 15)
        self.assertIn("10 + 5 = 15", history.get_history()[-1])


if __name__ == "__main__":
    unittest.main()
