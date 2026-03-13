import unittest

from prompt_regression_min.core import _score


class ContainsStepsAliasTests(unittest.TestCase):
    def test_contains_steps_alias_matches_ordered_values(self) -> None:
        self.assertTrue(
            _score(
                "collect analyze decide",
                {"type": "contains_steps", "values": ["collect", "decide"]},
            )
        )

    def test_contains_steps_ci_alias_matches_ignoring_case(self) -> None:
        self.assertTrue(
            _score(
                "Collect analyze DECIDE",
                {"type": "contains_steps_ci", "values": ["collect", "decide"]},
            )
        )


if __name__ == "__main__":
    unittest.main()
