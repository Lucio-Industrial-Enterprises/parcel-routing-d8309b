import subprocess
import sys
import unittest
from pathlib import Path


class CliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, "-m", "warehouse.cli", *args],
            cwd=Path(__file__).resolve().parents[1],
            capture_output=True,
            text=True,
        )

    def test_quotes(self):
        for zone, service_args, expected in (
            ("local", (), "$8.00\n"),
            ("regional", (), "$11.00\n"),
            ("local", ("--service", "standard"), "$8.00\n"),
            ("regional", ("--service", "standard"), "$11.00\n"),
            ("local", ("--service", "express"), "$15.00\n"),
            ("regional", ("--service", "express"), "$18.00\n"),
        ):
            with self.subTest(zone=zone, service_args=service_args):
                result = self.run_cli("2", zone, *service_args)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, expected)

    def test_unknown_service(self):
        result = self.run_cli("2", "local", "--service", "overnight")
        self.assertEqual(result.returncode, 2)
        self.assertIn("invalid choice", result.stderr)
        self.assertEqual(result.stdout, "")
