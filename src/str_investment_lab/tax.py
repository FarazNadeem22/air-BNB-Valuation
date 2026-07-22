from __future__ import annotations

from str_investment_lab.models import PropertyCandidate, TaxEstimate, TaxScenario


def estimate_accelerated_depreciation(
    property_candidate: PropertyCandidate,
    scenario: TaxScenario,
) -> TaxEstimate:
    """Estimate cost-seg-style first-year depreciation for CPA review."""
    land_value = property_candidate.purchase_price * scenario.land_value_rate
    depreciable_basis = property_candidate.purchase_price - land_value
    personal_property_basis = depreciable_basis * scenario.personal_property_rate
    bonus_depreciation = personal_property_basis * scenario.bonus_depreciation_rate

    return TaxEstimate(
        depreciable_building_basis=depreciable_basis,
        accelerated_personal_property_basis=personal_property_basis,
        first_year_bonus_depreciation=bonus_depreciation,
        review_required=scenario.review_required,
        note=(
            "Scenario estimate only. CPA must confirm STR nonpassive treatment, material "
            "participation, average guest stay, placed-in-service date, basis allocation, "
            "and cost segregation support."
        ),
    )

