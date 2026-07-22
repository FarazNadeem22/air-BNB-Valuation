from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class RevenueModel:
    model: Any
    feature_names: list[str]

    def predict_one(self, features: dict[str, float]) -> float:
        row = [[features[name] for name in self.feature_names]]
        return float(self.model.predict(row)[0])


def train_random_forest_revenue_model(
    rows: list[dict[str, float]],
    target_name: str = "annual_revenue",
) -> RevenueModel:
    """Train an ensemble model when scikit-learn is installed."""
    try:
        from sklearn.ensemble import RandomForestRegressor
    except ImportError as exc:
        raise RuntimeError(
            "Install the ml extra to train models: pip install -e '.[ml]'"
        ) from exc

    if not rows:
        raise ValueError("At least one training row is required.")

    feature_names = [name for name in rows[0] if name != target_name]
    x = [[row[name] for name in feature_names] for row in rows]
    y = [row[target_name] for row in rows]

    model = RandomForestRegressor(
        n_estimators=250,
        min_samples_leaf=3,
        random_state=42,
    )
    model.fit(x, y)
    return RevenueModel(model=model, feature_names=feature_names)

