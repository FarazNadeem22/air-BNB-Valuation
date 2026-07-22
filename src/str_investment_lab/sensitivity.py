from __future__ import annotations

from collections.abc import Iterable

from str_investment_lab.models import (
    FinancingAssumption,
    OperatingAssumption,
    PropertyCandidate,
    RevenueAssumption,
)
from str_investment_lab.underwriting import (
    estimate_interest_rate_from_credit_score,
    underwrite_property,
)


CONFIDENCE_REVENUE_MULTIPLIERS = {
    0.50: 1.00,
    0.70: 0.92,
    0.80: 0.86,
    0.90: 0.78,
    0.95: 0.70,
}


def revenue_at_confidence(
    revenue: RevenueAssumption,
    confidence_level: float,
) -> RevenueAssumption:
    multiplier = CONFIDENCE_REVENUE_MULTIPLIERS.get(confidence_level)
    if multiplier is None:
        raise ValueError(f"Unsupported confidence level: {confidence_level}")

    return RevenueAssumption(
        average_daily_rate=revenue.average_daily_rate * multiplier,
        occupancy_rate=revenue.occupancy_rate * multiplier,
        cleaning_fee_revenue_monthly=revenue.cleaning_fee_revenue_monthly,
        platform_fee_rate=revenue.platform_fee_rate,
    )


def build_sensitivity_matrix(
    property_candidate: PropertyCandidate,
    base_revenue: RevenueAssumption,
    operating: OperatingAssumption,
    down_payment_rates: Iterable[float],
    credit_scores: Iterable[int],
    confidence_levels: Iterable[float],
    base_interest_rate: float = 0.065,
) -> list[dict[str, float | int | str]]:
    rows: list[dict[str, float | int | str]] = []

    for down_payment_rate in down_payment_rates:
        for credit_score in credit_scores:
            interest_rate = estimate_interest_rate_from_credit_score(
                credit_score,
                base_rate=base_interest_rate,
            )
            for confidence_level in confidence_levels:
                adjusted_revenue = revenue_at_confidence(base_revenue, confidence_level)
                result = underwrite_property(
                    property_candidate=property_candidate,
                    revenue=adjusted_revenue,
                    operating=operating,
                    financing=FinancingAssumption(
                        down_payment_rate=down_payment_rate,
                        annual_interest_rate=interest_rate,
                        credit_score=credit_score,
                    ),
                )
                rows.append(
                    {
                        "address": property_candidate.address,
                        "down_payment_rate": down_payment_rate,
                        "credit_score": credit_score,
                        "confidence_level": confidence_level,
                        "interest_rate": interest_rate,
                        "annual_revenue": result.annual_revenue,
                        "annual_cash_flow": result.annual_cash_flow,
                        "cash_on_cash_return": result.cash_on_cash_return,
                        "dscr": result.dscr,
                        "breakeven_occupancy": result.breakeven_occupancy,
                    }
                )

    return rows

