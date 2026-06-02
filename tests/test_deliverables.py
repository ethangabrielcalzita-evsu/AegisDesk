"""
tests/test_deliverables.py
Example-based tests for the AegisDesk security deliverables.

Run from the project root:
    python -m pytest tests/test_deliverables.py -v
"""

import json
import os
import unittest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COLLECTION_FILE = os.path.join(ROOT_DIR, "AegisDesk_API_Collection.json")

POSTMAN_SCHEMA = "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"


def _load_collection() -> dict:
    with open(COLLECTION_FILE, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Postman collection tests (Examples 1–3 from design)
# ---------------------------------------------------------------------------

class TestPostmanCollectionStructure(unittest.TestCase):
    """Example 1 — schema, item count, and collection variables."""

    @classmethod
    def setUpClass(cls):
        cls.collection = _load_collection()

    # Req 1.7 — valid JSON and correct schema
    def test_file_exists_and_is_valid_json(self):
        self.assertTrue(os.path.isfile(COLLECTION_FILE), "Collection file not found")
        # _load_collection() would have raised an exception if JSON was invalid

    def test_schema_is_v2_1(self):
        self.assertEqual(self.collection["info"]["schema"], POSTMAN_SCHEMA)

    # Req 1.1–1.5 — exactly 5 request items
    def test_exactly_five_items(self):
        self.assertEqual(len(self.collection["item"]), 5)

    # Req 1.6, 2.1 — base_url and access_token collection variables
    def test_base_url_variable(self):
        keys = [v["key"] for v in self.collection["variable"]]
        self.assertIn("base_url", keys)

    def test_base_url_default_value(self):
        var = next(v for v in self.collection["variable"] if v["key"] == "base_url")
        self.assertEqual(var["value"], "http://127.0.0.1:8000")

    def test_access_token_variable_present(self):
        keys = [v["key"] for v in self.collection["variable"]]
        self.assertIn("access_token", keys)

    # Req 1.1 — obtain-token item present
    def test_obtain_token_item_present(self):
        names = [item["name"] for item in self.collection["item"]]
        self.assertIn("Obtain JWT Token", names)

    # Req 1.2 — refresh-token item present
    def test_refresh_token_item_present(self):
        names = [item["name"] for item in self.collection["item"]]
        self.assertIn("Refresh JWT Token", names)

    # Req 1.3 — authenticated log-incident item present
    def test_authenticated_log_incident_present(self):
        names = [item["name"] for item in self.collection["item"]]
        self.assertIn("Log Incident (Authenticated)", names)

    # Req 1.4 — unauthenticated log-incident item present
    def test_unauthenticated_log_incident_present(self):
        names = [item["name"] for item in self.collection["item"]]
        self.assertIn("Log Incident (Unauthenticated — expects 401)", names)

    # Req 1.5 — missing-title log-incident item present
    def test_missing_title_log_incident_present(self):
        names = [item["name"] for item in self.collection["item"]]
        self.assertIn("Log Incident (Missing title — expects 400)", names)

    # Req 1.6 — all URLs reference {{base_url}}
    def test_all_urls_use_base_url_variable(self):
        for item in self.collection["item"]:
            raw_url = item["request"]["url"]["raw"]
            self.assertIn("{{base_url}}", raw_url, f"Item '{item['name']}' URL missing {{base_url}}")


class TestPostmanTokenTestScript(unittest.TestCase):
    """Example 2 — token test script writes access_token (Req 2.2)."""

    @classmethod
    def setUpClass(cls):
        collection = _load_collection()
        cls.obtain_item = next(
            i for i in collection["item"] if i["name"] == "Obtain JWT Token"
        )

    def test_test_event_exists(self):
        event_names = [e["listen"] for e in self.obtain_item.get("event", [])]
        self.assertIn("test", event_names)

    def test_test_script_sets_access_token(self):
        test_event = next(e for e in self.obtain_item["event"] if e["listen"] == "test")
        exec_lines = test_event["script"]["exec"]
        full_script = " ".join(exec_lines)
        self.assertIn("pm.collectionVars.set", full_script)
        self.assertIn("access_token", full_script)


class TestPostmanAuthenticatedHeader(unittest.TestCase):
    """Example 3 — authenticated request carries Bearer {{access_token}} (Req 2.3)."""

    @classmethod
    def setUpClass(cls):
        collection = _load_collection()
        cls.auth_item = next(
            i for i in collection["item"] if i["name"] == "Log Incident (Authenticated)"
        )

    def test_authorization_header_present(self):
        header_keys = [h["key"] for h in self.auth_item["request"]["header"]]
        self.assertIn("Authorization", header_keys)

    def test_authorization_header_uses_bearer_token(self):
        auth_header = next(
            h for h in self.auth_item["request"]["header"] if h["key"] == "Authorization"
        )
        self.assertEqual(auth_header["value"], "Bearer {{access_token}}")


if __name__ == "__main__":
    unittest.main()


# ---------------------------------------------------------------------------
# Audit report tests (Examples 4–6 from design)
# ---------------------------------------------------------------------------

import subprocess
import tempfile
import importlib
import sys
from unittest.mock import patch, MagicMock


def _run_generate_audit(tmp_dir: str) -> None:
    """
    Import generate_audit_report and run its main() with the working
    directory and output paths redirected to *tmp_dir*.
    """
    import generate_audit_report as gar

    # Patch os.path.dirname(os.path.abspath(__file__)) → tmp_dir so both
    # output files land inside our temporary directory.
    with patch("generate_audit_report.os.path.abspath", return_value=os.path.join(tmp_dir, "generate_audit_report.py")):
        with patch("generate_audit_report.os.path.dirname", return_value=tmp_dir):
            gar.main()


class TestAuditReportGeneration(unittest.TestCase):
    """Examples 4–5 — PDF and raw text created with expected content."""

    MOCK_OUTPUT = "mock scan output line"

    def _run_with_mock_subprocess(self, tmp_dir: str) -> None:
        import generate_audit_report as gar

        mock_result = MagicMock()
        mock_result.stdout = self.MOCK_OUTPUT

        with patch("generate_audit_report.subprocess.run", return_value=mock_result):
            with patch(
                "generate_audit_report.os.path.abspath",
                return_value=os.path.join(tmp_dir, "generate_audit_report.py"),
            ):
                with patch("generate_audit_report.os.path.dirname", return_value=tmp_dir):
                    gar.main()

    # Req 6.1, 6.5 — PDF file is created
    def test_pdf_file_is_created(self):
        import generate_audit_report  # noqa: ensure importable
        with tempfile.TemporaryDirectory() as tmp:
            self._run_with_mock_subprocess(tmp)
            pdf_path = os.path.join(tmp, "AegisDesk_Security_Audit_Report.pdf")
            self.assertTrue(os.path.isfile(pdf_path), "PDF report was not created")

    # Req 3.3, 4.3, 5.2 — raw text contains all section labels
    def test_raw_text_contains_pip_audit_section(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run_with_mock_subprocess(tmp)
            raw = open(os.path.join(tmp, "audit_report_raw.txt"), encoding="utf-8").read()
            self.assertIn("Dependency Vulnerability Scan (pip-audit)", raw)

    def test_raw_text_contains_bandit_section(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run_with_mock_subprocess(tmp)
            raw = open(os.path.join(tmp, "audit_report_raw.txt"), encoding="utf-8").read()
            self.assertIn("Static Code Analysis (bandit)", raw)

    def test_raw_text_contains_deploy_check_section(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run_with_mock_subprocess(tmp)
            raw = open(os.path.join(tmp, "audit_report_raw.txt"), encoding="utf-8").read()
            self.assertIn("Django Deployment Security Check (check --deploy)", raw)

    # Req 6.2 — cover strings present
    def test_raw_text_contains_project_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run_with_mock_subprocess(tmp)
            raw = open(os.path.join(tmp, "audit_report_raw.txt"), encoding="utf-8").read()
            self.assertIn("AegisDesk", raw)

    def test_raw_text_contains_report_title(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run_with_mock_subprocess(tmp)
            raw = open(os.path.join(tmp, "audit_report_raw.txt"), encoding="utf-8").read()
            self.assertIn("Security Audit Log", raw)


class TestAuditReportMissingTool(unittest.TestCase):
    """Example 6 — graceful handling when a tool is not on PATH (Req 3.2, 4.2)."""

    def _run_with_tool_missing(self, tmp_dir: str) -> None:
        import generate_audit_report as gar

        def _side_effect(cmd, **kwargs):
            if cmd[0] in ("pip-audit", "bandit"):
                raise FileNotFoundError(f"No such file: {cmd[0]}")
            # manage.py check --deploy succeeds normally
            result = MagicMock()
            result.stdout = "System check identified no issues."
            return result

        with patch("generate_audit_report.subprocess.run", side_effect=_side_effect):
            with patch(
                "generate_audit_report.os.path.abspath",
                return_value=os.path.join(tmp_dir, "generate_audit_report.py"),
            ):
                with patch("generate_audit_report.os.path.dirname", return_value=tmp_dir):
                    gar.main()

    # Req 3.2, 4.2 — error message in raw text, no traceback crash
    def test_missing_tool_produces_error_message_not_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run_with_tool_missing(tmp)
            raw = open(os.path.join(tmp, "audit_report_raw.txt"), encoding="utf-8").read()
            self.assertIn("[ERROR] Tool not found", raw)

    def test_script_still_creates_pdf_when_tool_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run_with_tool_missing(tmp)
            pdf_path = os.path.join(tmp, "AegisDesk_Security_Audit_Report.pdf")
            self.assertTrue(os.path.isfile(pdf_path), "PDF should still be created when a tool is missing")
