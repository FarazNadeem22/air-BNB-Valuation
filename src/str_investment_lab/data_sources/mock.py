from __future__ import annotations

from str_investment_lab.data_sources.base import PropertyDataSource, RevenueDataSource
from str_investment_lab.models import PropertyCandidate, RevenueAssumption


class MockPropertyDataSource(PropertyDataSource):
    def lookup_property(self, address: str) -> PropertyCandidate:
        return PropertyCandidate(
            address=address,
            city="Scottsdale",
            state="AZ",
            purchase_price=725000,
            bedrooms=4,
            bathrooms=3.0,
            square_feet=2200,
            annual_property_tax=5200,
            annual_insurance=2600,
            hoa_monthly=120,
        )


class MockRevenueDataSource(RevenueDataSource):
    def estimate_revenue(self, address: str, bedrooms: int, bathrooms: float) -> RevenueAssumption:
        return RevenueAssumption(
            average_daily_rate=315,
            occupancy_rate=0.68,
            cleaning_fee_revenue_monthly=900,
        )

