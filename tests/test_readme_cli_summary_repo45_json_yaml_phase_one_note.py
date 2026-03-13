from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryRepo45JsonYamlPhaseOneNoteTests(unittest.TestCase):
    def test_readme_mentions_cli_summary_repo45_json_yaml_phase_one_note(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')

        self.assertIn('docs/CLI_SUMMARY_REPO45_JSON_YAML_PHASE_ONE_NOTE.md', readme)
        self.assertTrue((ROOT / 'docs' / 'CLI_SUMMARY_REPO45_JSON_YAML_PHASE_ONE_NOTE.md').exists())


if __name__ == '__main__':
    unittest.main()
