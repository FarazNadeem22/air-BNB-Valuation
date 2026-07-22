from __future__ import annotations

import csv
from pathlib import Path

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


def _float(row: dict[str, str], field_name: str, default: float | None = None) -> float:
    raw_value = row.get(field_name, "")
    if raw_value == "" and default is not None:
        return default
    return float(raw_value)


def _int(row: dict[str, str], field_name: str, default: int | None = None) -> int:
    raw_value = row.get(field_name, "")
    if raw_value == "" and default is not None:
        return default
    return int(raw_value)


def row_to_property(row: dict[str, str]) -> PropertyCandidate:
    return PropertyCandidate(
        address=row["address"],
        city=row["city"],
        state=row["state"],
        purchase_price=_float(row, "purchase_price"),
        bedrooms=_int(row, "bedrooms"),
        bathrooms=_float(row, "bathrooms"),
        square_feet=_int(row, "square_feet"),
        annual_property_tax=_float(row, "annual_property_tax"),
        annual_insurance=_float(row, "annual_insurance"),
        hoa_monthly=_float(row, "hoa_monthly", 0.0),
    )


def row_to_revenue(row: dict[str, str]) -> RevenueAssumption:
    return RevenueAssumption(
        average_daily_rate=_float(row, "average_daily_rate"),
        occupancy_rate=_float(row, "occupancy_rate"),
        cleaning_fee_revenue_monthly=_float(row, "cleaning_fee_revenue_monthly", 0.0),
        platform_fee_rate=_float(row, "platform_fee_rate", 0.03),
    )


def row_to_financing(row: dict[str, str]) -> FinancingAssumption:
    credit_score = _int(row, "credit_score", 740)
    interest_rate = _float(
        row,
        "annual_interest_rate",
        estimate_interest_rate_from_credit_score(credit_score),
    )
    return FinancingAssumption(
        down_payment_rate=_float(row, "down_payment_rate", 0.20),
        annual_interest_rate=interest_rate,
        amortization_years=_int(row, "amortization_years", 30),
        closing_cost_rate=_float(row, "closing_cost_rate", 0.035),
        furnishing_budget=_float(row, "furnishing_budget", 35000.0),
        credit_score=credit_score,
    )


def analyze_csv(path: str | Path) -> list[dict[str, float | int | str]]:
    csv_path = Path(path)
    rows: list[dict[str, float | int | str]] = []
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            property_candidate = row_to_property(row)
            revenue = row_to_revenue(row)
            financing = row_to_financing(row)
            result = underwrite_property(
                property_candidate=property_candidate,
                revenue=revenue,
                operating=OperatingAssumption(),
                financing=financing,
            )
            rows.append(
                {
                    "address": result.address,
                    "purchase_price": result.purchase_price,
                    "credit_score": financing.credit_score,
                    "down_payment_rate": financing.down_payment_rate,
                    "annual_revenue": round(result.annual_revenue, 2),
                    "annual_cash_flow": round(result.annual_cash_flow, 2),
                    "cap_rate": round(result.cap_rate, 4),
                    "cash_on_cash_return": round(result.cash_on_cash_return, 4),
                    "dscr": round(result.dscr, 3),
                    "breakeven_occupancy": round(result.breakeven_occupancy, 4),
                }
            )
    return rows

