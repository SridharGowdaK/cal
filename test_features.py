import builtins
import unittest
from unittest.mock import patch

from app import main
from calculator import add, subtract, multiply, divide
from login import LoginSystem


class FeatureTests(unittest.TestCase):
    def test_calculator_basic_operations(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(subtract(10, 4), 6)
        self.assertEqual(multiply(3, 4), 12)
        self.assertEqual(divide(8, 2), 4)

    def test_login_system(self):
        auth = LoginSystem()
        auth.register_user("alice", "secret123")
        self.assertTrue(auth.login("alice", "secret123"))
        self.assertFalse(auth.login("alice", "wrongpass"))

    def test_main_handles_eof(self):
        with patch.object(builtins, "input", side_effect=EOFError):
            main()


if __name__ == "__main__":
    unittest.main()
