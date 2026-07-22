from __future__ import annotations

from abc import ABC, abstractmethod

from str_investment_lab.models import PropertyCandidate, RevenueAssumption


class PropertyDataSource(ABC):
    @abstractmethod
    def lookup_property(self, address: str) -> PropertyCandidate:
        raise NotImplementedError


class RevenueDataSource(ABC):
    @abstractmethod
    def estimate_revenue(self, address: str, bedrooms: int, bathrooms: float) -> RevenueAssumption:
        raise NotImplementedError

