"""Unit-тесты для расчета чистой нефти (DailyProduction.net_oil)."""
import pytest
from app.models import DailyProduction


@pytest.mark.parametrize(
    "liquid_produced, water_cut, density, expected_net_oil",
    [
        pytest.param(500, 20, 1.0, 400, id="basic_case"),
        pytest.param(1000, 0, 1.0, 1000, id="no_water_cut_equals_liquid_produced"),
        pytest.param(1000, 100, 1.0, 0, id="full_water_cut_gives_zero"),
        pytest.param(250, 50, 0.85, 106.25, id="basic_case_with_density"),
        pytest.param(100, 25, 0.85, 63.75, id="realistic_density_low_volume"),
        pytest.param(750, 10, 0.9, 607.5, id="realistic_density_high_volume"),
        pytest.param(0, 20, 0.85, 0, id="zero_liquid_produced_gives_zero"),
        pytest.param(500, 0, 0, 0, id="zero_density_gives_zero"),
        pytest.param(500, 20, 100, 40000, id="density_scales_result_linearly"),
        pytest.param(333.33, 33, 0.87, 194.298057, id="fractional_values_precision"),
    ],
)
def test_net_oil_property(liquid_produced, water_cut, density, expected_net_oil):
    """Проверяет расчет net_oil по формуле liquid_produced * (1 - water_cut/100) * density
    для набора базовых, реалистичных, граничных и дробных значений.
    """
    record = DailyProduction(
        liquid_produced=liquid_produced,
        water_cut=water_cut,
        density=density,
    )
    assert record.net_oil == pytest.approx(expected_net_oil, rel=1e-4)


def test_net_oil_is_never_negative_for_valid_water_cut_range():
    """При water_cut в допустимом диапазоне (0-100) net_oil не должен быть отрицательным."""
    record = DailyProduction(liquid_produced=500, water_cut=100, density=0.85)
    assert record.net_oil >= 0


def test_net_oil_scales_linearly_with_liquid_produced():
    """При фиксированных water_cut и density net_oil должен расти пропорционально liquid_produced."""
    base = DailyProduction(liquid_produced=100, water_cut=20, density=0.85)
    doubled = DailyProduction(liquid_produced=200, water_cut=20, density=0.85)
    assert doubled.net_oil == pytest.approx(base.net_oil * 2, rel=1e-6)


def test_net_oil_scales_linearly_with_density():
    """При фиксированных liquid_produced и water_cut net_oil должен расти пропорционально density."""
    base = DailyProduction(liquid_produced=500, water_cut=20, density=0.85)
    doubled_density = DailyProduction(liquid_produced=500, water_cut=20, density=1.7)
    assert doubled_density.net_oil == pytest.approx(base.net_oil * 2, rel=1e-6)


def test_net_oil_decreases_as_water_cut_increases():
    """При росте обводненности объем чистой нефти должен монотонно снижаться."""
    low_water_cut = DailyProduction(liquid_produced=500, water_cut=10, density=0.85)
    high_water_cut = DailyProduction(liquid_produced=500, water_cut=90, density=0.85)
    assert high_water_cut.net_oil < low_water_cut.net_oil