import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from datetime import datetime
from main import status

NOW = datetime(2026, 10, 31, 12, 0, 0)


class TestBackupAge(unittest.TestCase):
    def test_breached(self):
        self.assertEqual(status("2026-10-30T00:00:00", 24, NOW)[0], "BREACHED")

    def test_at_risk(self):
        self.assertEqual(status("2026-10-30T16:00:00", 24, NOW)[0], "AT RISK")

    def test_ok(self):
        self.assertEqual(status("2026-10-31T11:00:00", 24, NOW)[0], "OK")
