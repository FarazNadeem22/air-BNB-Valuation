import unittest

from str_investment_lab.models import (
    FinancingAssumption,
    OperatingAssumption,
    PropertyCandidate,
    RevenueAssumption,
    TaxScenario,
)
from str_investment_lab.sensitivity import build_sensitivity_matrix
from str_investment_lab.tax import estimate_accelerated_depreciation
from str_investment_lab.underwriting import (
    estimate_interest_rate_from_credit_score,
    monthly_mortgage_payment,
    underwrite_property,
)


class UnderwritingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.property_candidate = PropertyCandidate(
            address="123 Test Street",
            city="Scottsdale",
            state="AZ",
            purchase_price=725000,
            bedrooms=4,
            bathrooms=3,
            square_feet=2200,
            annual_property_tax=5200,
            annual_insurance=2600,
            hoa_monthly=120,
        )
        self.revenue = RevenueAssumption(
            average_daily_rate=315,
            occupancy_rate=0.68,
            cleaning_fee_revenue_monthly=900,
        )
        self.operating = OperatingAssumption()

    def test_mortgage_payment_is_positive(self) -> None:
        payment = monthly_mortgage_payment(580000, 0.065, 30)
        self.assertGreater(payment, 0)
        self.assertAlmostEqual(payment, 3665.99, places=2)

    def test_credit_score_curve_improves_with_higher_score(self) -> None:
        self.assertLess(
            estimate_interest_rate_from_credit_score(780),
            estimate_interest_rate_from_credit_score(660),
        )

    def test_underwriting_outputs_key_metrics(self) -> None:
        result = underwrite_property(
            self.property_candidate,
            self.revenue,
            self.operating,
            FinancingAssumption(
                down_payment_rate=0.20,
                annual_interest_rate=0.065,
            ),
        )
        self.assertEqual(result.address, "123 Test Street")
        self.assertGreater(result.annual_revenue, 0)
        self.assertGreater(result.cash_to_close, result.down_payment)
        self.assertGreater(result.breakeven_occupancy, 0)

    def test_sensitivity_matrix_shape(self) -> None:
        rows = build_sensitivity_matrix(
            self.property_candidate,
            self.revenue,
            self.operating,
            down_payment_rates=[0.20, 0.25],
            credit_scores=[700, 740],
            confidence_levels=[0.50, 0.90],
        )
        self.assertEqual(len(rows), 8)
        self.assertIn("cash_on_cash_return", rows[0])

    def test_tax_estimate_marks_cpa_review(self) -> None:
        estimate = estimate_accelerated_depreciation(
            self.property_candidate,
            TaxScenario(),
        )
        self.assertTrue(estimate.review_required)
        self.assertGreater(estimate.first_year_bonus_depreciation, 0)


if __name__ == "__main__":
    unittest.main()
