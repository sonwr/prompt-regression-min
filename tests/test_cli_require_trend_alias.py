import unittest

from prompt_regression_min.cli import _build_parser


class CliRequireTrendAliasTests(unittest.TestCase):
    def test_require_trend_alias_maps_to_pass_rate_gate(self) -> None:
        parser = _build_parser()
        args = parser.parse_args([
            "run",
            "--dataset", "dataset.jsonl",
            "--baseline", "baseline.jsonl",
            "--candidate", "candidate.jsonl",
            "--require-trend", "flat",
        ])
        self.assertEqual(args.require_pass_rate_trend, "flat")


if __name__ == "__main__":
    unittest.main()
