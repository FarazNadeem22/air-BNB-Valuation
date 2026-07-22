import unittest

from str_investment_lab.csv_ingestion import analyze_csv


class CsvIngestionTests(unittest.TestCase):
    def test_analyze_csv_returns_underwriting_rows(self) -> None:
        rows = analyze_csv("data/sample_properties.csv")
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["address"], "123 Portfolio Demo Lane")
        self.assertIn("cash_on_cash_return", rows[0])
        self.assertIn("breakeven_occupancy", rows[0])


if __name__ == "__main__":
    unittest.main()

