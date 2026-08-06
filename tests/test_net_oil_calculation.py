"""Unit-тесты для расчета чистой нефти (DailyProduction.net_oil)."""
import pytest
from app.models import DailyProduction


@pytest.mark.parametrize(
    "liquid_produced, water_cut, density, expected_net_oil",
    [
        (500, 20, 1.0, 400),      # 500 * 0.80 * 1.0
        (1000, 0, 1.0, 1000),     # нет обводненности -> net_oil == liquid_produced
        (1000, 100, 1.0, 0),      # 100% обводненность -> net_oil == 0
        (250, 50, 0.85, 106.25),  # 250 * 0.50 * 0.85
        (0, 20, 1.0, 0),          # нулевая добыча -> net_oil == 0
    ],
)
def test_net_oil_property(liquid_produced, water_cut, density, expected_net_oil):
    record = DailyProduction(
        liquid_produced=liquid_produced,
        water_cut=water_cut,
        density=density,
    )
    assert record.net_oil == pytest.approx(expected_net_oil, rel=1e-6)