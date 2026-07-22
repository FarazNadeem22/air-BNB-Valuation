from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PropertyCandidate:
    address: str
    city: str
    state: str
    purchase_price: float
    bedrooms: int
    bathrooms: float
    square_feet: int
    annual_property_tax: float
    annual_insurance: float
    hoa_monthly: float = 0.0


@dataclass(frozen=True)
class RevenueAssumption:
    average_daily_rate: float
    occupancy_rate: float
    cleaning_fee_revenue_monthly: float = 0.0
    platform_fee_rate: float = 0.03

    @property
    def annual_gross_booking_revenue(self) -> float:
        return self.average_daily_rate * 365 * self.occupancy_rate


@dataclass(frozen=True)
class OperatingAssumption:
    property_management_rate: float = 0.18
    repairs_and_maintenance_rate: float = 0.05
    utilities_monthly: float = 550.0
    supplies_monthly: float = 250.0
    cleaning_expense_monthly: float = 700.0
    capex_reserve_rate: float = 0.05


@dataclass(frozen=True)
class FinancingAssumption:
    down_payment_rate: float
    annual_interest_rate: float
    amortization_years: int = 30
    closing_cost_rate: float = 0.035
    furnishing_budget: float = 35000.0
    credit_score: int = 740


@dataclass(frozen=True)
class UnderwritingResult:
    address: str
    purchase_price: float
    down_payment: float
    loan_amount: float
    cash_to_close: float
    annual_revenue: float
    annual_operating_expenses: float
    annual_debt_service: float
    annual_cash_flow: float
    noi: float
    cap_rate: float
    cash_on_cash_return: float
    dscr: float
    breakeven_occupancy: float


@dataclass(frozen=True)
class TaxScenario:
    land_value_rate: float = 0.20
    personal_property_rate: float = 0.18
    bonus_depreciation_rate: float = 1.00
    review_required: bool = True


@dataclass(frozen=True)
class TaxEstimate:
    depreciable_building_basis: float
    accelerated_personal_property_basis: float
    first_year_bonus_depreciation: float
    review_required: bool
    note: str

