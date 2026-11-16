"""Smoke checks that the published demo can be reproduced end to end."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from generate_data import generate  # noqa: E402
from analyze import build_db, run  # noqa: E402


class TestOperationsAnalysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        generate()

    def test_every_payment_has_one_status(self):
        conn = build_db()
        n = conn.execute("SELECT COUNT(*) FROM payments").fetchone()[0]
        invalid = conn.execute("SELECT COUNT(*) FROM payments WHERE status NOT IN ('approved','declined')").fetchone()[0]
        conn.close()
        self.assertEqual(n, 4800)
        self.assertEqual(invalid, 0)

    def test_no_unmatched_tickets(self):
        conn = build_db()
        unmatched = conn.execute("""SELECT COUNT(*) FROM support_tickets t
            LEFT JOIN payments p ON p.payment_id=t.payment_id WHERE p.payment_id IS NULL""").fetchone()[0]
        conn.close()
        self.assertEqual(unmatched, 0)

    def test_summary(self):
        result = run()
        self.assertEqual(result["payments"], 4800)
        self.assertTrue(0 < result["approval_pct"] < 100)
        self.assertTrue((ROOT / "reports" / "analysis.md").exists())


if __name__ == "__main__":
    unittest.main()
