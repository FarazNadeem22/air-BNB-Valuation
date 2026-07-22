from __future__ import annotations

from dataclasses import dataclass

from str_investment_lab.data_sources.base import RevenueDataSource
from str_investment_lab.models import RevenueAssumption


@dataclass(frozen=True)
class AirDnaClient(RevenueDataSource):
    api_key: str
    base_url: str = "https://api.airdna.co"

    def estimate_revenue(self, address: str, bedrooms: int, bathrooms: float) -> RevenueAssumption:
        raise NotImplementedError(
            "Wire this method to the AirDNA Enterprise API package you license. "
            "Keep raw responses in data/raw and normalize into RevenueAssumption."
        )

