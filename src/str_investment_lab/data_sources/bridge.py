from __future__ import annotations

from dataclasses import dataclass

from str_investment_lab.data_sources.base import PropertyDataSource
from str_investment_lab.models import PropertyCandidate


@dataclass(frozen=True)
class BridgeClient(PropertyDataSource):
    token: str
    base_url: str = "https://api.bridgedataoutput.com"

    def lookup_property(self, address: str) -> PropertyCandidate:
        raise NotImplementedError(
            "Bridge/Zillow access is approval-based. Implement this after receiving "
            "authorized MLS, public records, or Zestimate dataset access."
        )

