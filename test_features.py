import builtins
import os
import tempfile
import unittest
from unittest.mock import patch

from ai_service import (
    ai_assistant_chat,
    audit_password_security,
    solve_natural_language_math,
)
from app import main
from calculator import (
    CalculatorHistory,
    add,
    calculate,
    divide,
    modulus,
    multiply,
    percentage,
    power,
    square_root,
    subtract,
)
from login import (
    LoginPage,
    LoginSystem,
    generate_password,
    hash_password,
    password_strength,
    verify_password,
)
from web_app import app as flask_app


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

    def test_ai_math_solver(self):
        # Percentage
        pct_res = solve_natural_language_math("What is 15 percent of 850?")
        self.assertTrue(pct_res["success"])
        self.assertEqual(pct_res["result"], "127.5")

        # Equation solving
        eq_res = solve_natural_language_math("solve 2*x + 6 = 14")
        self.assertTrue(eq_res["success"])
        self.assertIn("4", eq_res["result"])

        # Square root
        sqrt_res = solve_natural_language_math("square root of 144 plus 25")
        self.assertTrue(sqrt_res["success"])
        self.assertEqual(sqrt_res["result"], "37")

        # Invalid expression
        err_res = solve_natural_language_math("invalid @#$%")
        self.assertFalse(err_res["success"])

    def test_ai_password_audit(self):
        audit = audit_password_security("Tr0ub4dor&3")
        self.assertTrue(audit["success"])
        self.assertGreater(audit["entropy_bits"], 30)
        self.assertIn("years", audit["estimated_crack_time"])

        weak_audit = audit_password_security("123456")
        self.assertTrue(weak_audit["success"])
        self.assertIn("Weak", weak_audit["security_level"])
        self.assertIn("Instant", weak_audit["estimated_crack_time"])

    def test_ai_assistant_chat(self):
        # Math query
        res = ai_assistant_chat("What is 20 + 30?")
        self.assertTrue(res["success"])
        self.assertIn("50", res["reply"])

        # Security query
        sec_res = ai_assistant_chat("How does PBKDF2 protect passwords?")
        self.assertTrue(sec_res["success"])
        self.assertIn("PBKDF2", sec_res["reply"])

    def test_flask_web_endpoints(self):
        client = flask_app.test_client()

        # Index route
        res = client.get("/")
        self.assertEqual(res.status_code, 200)

        # Calculate API
        calc_res = client.post("/api/calculate", json={"operation": "*", "a": 7, "b": 6})
        self.assertEqual(calc_res.status_code, 200)
        self.assertEqual(calc_res.get_json()["result"], 42.0)

        # AI Math API
        math_res = client.post("/api/ai/solve-math", json={"query": "square root of 81"})
        self.assertEqual(math_res.status_code, 200)
        self.assertEqual(math_res.get_json()["result"], "9")

        # AI Security Audit API
        audit_res = client.post("/api/ai/audit-password", json={"password": "MyStrongPassword#2026"})
        self.assertEqual(audit_res.status_code, 200)
        self.assertTrue(audit_res.get_json()["success"])

        # Password generate API
        gen_res = client.post("/api/password/generate", json={"length": 18})
        self.assertEqual(gen_res.status_code, 200)
        self.assertEqual(len(gen_res.get_json()["password"]), 18)


if __name__ == "__main__":
    unittest.main()
