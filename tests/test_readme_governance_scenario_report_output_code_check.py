from pathlib import Path
import unittest


class ReadmeGovernanceScenarioReportOutputCodeCheckTest(unittest.TestCase):
    def test_readme_mentions_governance_scenario_report_output_code_check(self) -> None:
        text = (Path(__file__).resolve().parents[1] / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/GOVERNANCE_SCENARIO_REPORT_OUTPUT_CODE_CHECK.md", text)


if __name__ == "__main__":
    unittest.main()
