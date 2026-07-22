from __future__ import annotations

import argparse
import json

from str_investment_lab.data_sources.mock import MockPropertyDataSource, MockRevenueDataSource
from str_investment_lab.models import OperatingAssumption, TaxScenario
from str_investment_lab.sensitivity import build_sensitivity_matrix
from str_investment_lab.tax import estimate_accelerated_depreciation


def sample_analysis() -> dict[str, object]:
    property_source = MockPropertyDataSource()
    revenue_source = MockRevenueDataSource()

    property_candidate = property_source.lookup_property("123 Portfolio Demo Lane")
    revenue = revenue_source.estimate_revenue(
        property_candidate.address,
        property_candidate.bedrooms,
        property_candidate.bathrooms,
    )
    operating = OperatingAssumption()

    matrix = build_sensitivity_matrix(
        property_candidate=property_candidate,
        base_revenue=revenue,
        operating=operating,
        down_payment_rates=[0.15, 0.20, 0.25, 0.30],
        credit_scores=[660, 700, 740, 780],
        confidence_levels=[0.50, 0.70, 0.80, 0.90],
    )
    tax_estimate = estimate_accelerated_depreciation(
        property_candidate,
        TaxScenario(),
    )

    return {
        "property": property_candidate.__dict__,
        "base_revenue": revenue.__dict__,
        "tax_estimate": tax_estimate.__dict__,
        "sensitivity_rows": matrix,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", action="store_true", help="Run the sample portfolio analysis.")
    args = parser.parse_args()

    if args.sample:
        print(json.dumps(sample_analysis(), indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

