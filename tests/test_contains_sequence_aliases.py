import unittest

from prompt_regression_min.core import _score


class ContainsSequenceAliasTests(unittest.TestCase):
    def test_contains_sequence_alias_matches_ordered_values(self) -> None:
        self.assertTrue(
            _score(
                "alpha middle omega",
                {"type": "contains_sequence", "values": ["alpha", "omega"]},
            )
        )

    def test_contains_sequence_ci_alias_matches_ignoring_case(self) -> None:
        self.assertTrue(
            _score(
                "Alpha middle OMEGA",
                {"type": "contains_sequence_ci", "values": ["alpha", "omega"]},
            )
        )


if __name__ == "__main__":
    unittest.main()
