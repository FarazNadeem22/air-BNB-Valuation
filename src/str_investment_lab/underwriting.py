from __future__ import annotations

from str_investment_lab.models import (
    FinancingAssumption,
    OperatingAssumption,
    PropertyCandidate,
    RevenueAssumption,
    UnderwritingResult,
)


def monthly_mortgage_payment(principal: float, annual_interest_rate: float, years: int) -> float:
    """Calculate fixed-rate monthly principal and interest payment."""
    if principal <= 0:
        return 0.0

    months = years * 12
    monthly_rate = annual_interest_rate / 12
    if monthly_rate == 0:
        return principal / months

    return principal * (monthly_rate * (1 + monthly_rate) ** months) / (
        (1 + monthly_rate) ** months - 1
    )


def estimate_interest_rate_from_credit_score(
    credit_score: int,
    base_rate: float = 0.065,
) -> float:
    """Simple portfolio demo rate curve. Replace with a lender/API feed for production."""
    if credit_score >= 780:
        spread = -0.0025
    elif credit_score >= 740:
        spread = 0.0
    elif credit_score >= 700:
        spread = 0.0040
    elif credit_score >= 660:
        spread = 0.0080
    elif credit_score >= 620:
        spread = 0.0140
    else:
        spread = 0.0225
    return base_rate + spread


def annual_operating_expenses(
    property_candidate: PropertyCandidate,
    revenue: RevenueAssumption,
    operating: OperatingAssumption,
) -> float:
    annual_revenue = revenue.annual_gross_booking_revenue + revenue.cleaning_fee_revenue_monthly * 12
    variable_expenses = annual_revenue * (
        operating.property_management_rate
        + operating.repairs_and_maintenance_rate
        + operating.capex_reserve_rate
        + revenue.platform_fee_rate
    )
    fixed_expenses = (
        property_candidate.annual_property_tax
        + property_candidate.annual_insurance
        + property_candidate.hoa_monthly * 12
        + operating.utilities_monthly * 12
        + operating.supplies_monthly * 12
        + operating.cleaning_expense_monthly * 12
    )
    return variable_expenses + fixed_expenses


def underwrite_property(
    property_candidate: PropertyCandidate,
    revenue: RevenueAssumption,
    operating: OperatingAssumption,
    financing: FinancingAssumption,
) -> UnderwritingResult:
    annual_revenue = revenue.annual_gross_booking_revenue + revenue.cleaning_fee_revenue_monthly * 12
    down_payment = property_candidate.purchase_price * financing.down_payment_rate
    loan_amount = property_candidate.purchase_price - down_payment
    cash_to_close = (
        down_payment
        + property_candidate.purchase_price * financing.closing_cost_rate
        + financing.furnishing_budget
    )

    debt_service = (
        monthly_mortgage_payment(
            loan_amount,
            financing.annual_interest_rate,
            financing.amortization_years,
        )
        * 12
    )
    operating_expenses = annual_operating_expenses(property_candidate, revenue, operating)
    noi = annual_revenue - operating_expenses
    cash_flow = noi - debt_service

    cap_rate = noi / property_candidate.purchase_price
    cash_on_cash = cash_flow / cash_to_close if cash_to_close else 0.0
    dscr = noi / debt_service if debt_service else float("inf")

    daily_revenue_at_full_occupancy = revenue.average_daily_rate * 365
    breakeven_occupancy = (operating_expenses + debt_service) / daily_revenue_at_full_occupancy

    return UnderwritingResult(
        address=property_candidate.address,
        purchase_price=property_candidate.purchase_price,
        down_payment=down_payment,
        loan_amount=loan_amount,
        cash_to_close=cash_to_close,
        annual_revenue=annual_revenue,
        annual_operating_expenses=operating_expenses,
        annual_debt_service=debt_service,
        annual_cash_flow=cash_flow,
        noi=noi,
        cap_rate=cap_rate,
        cash_on_cash_return=cash_on_cash,
        dscr=dscr,
        breakeven_occupancy=breakeven_occupancy,
    )

