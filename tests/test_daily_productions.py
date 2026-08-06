"""Unit-тесты валидации формы CreateDailyProduction.

Проверяет только логику валидации (WTForms + кастомные валидаторы),
без обращения к контроллеру, роутингу или шаблонам.
"""
from app.forms import CreateDailyProduction


def _form_data(well_id, **overrides):
    data = {
        "well_id": well_id,
        "date": "2026-08-03",
        "operating_hours": 20,
        "liquid_produced": 500,
        "water_cut": 20,
        "density": 800,
    }
    data.update(overrides)
    return data


def test_rejects_operating_hours_over_24(app, well):
    with app.test_request_context(
        method="POST", data=_form_data(well, operating_hours=25)
    ):
        form = CreateDailyProduction()
        assert not form.validate()
        assert "operating_hours" in form.errors


def test_rejects_operating_hours_negative(app, well):
    with app.test_request_context(
        method="POST", data=_form_data(well, operating_hours=-1)
    ):
        form = CreateDailyProduction()
        assert not form.validate()
        assert "operating_hours" in form.errors


def test_accepts_operating_hours_lower_boundary_0(app, well):
    with app.test_request_context(
        method="POST", data=_form_data(well, operating_hours=0)
    ):
        form = CreateDailyProduction()
        assert form.validate()
        assert "operating_hours" not in form.errors


def test_accepts_operating_hours_upper_boundary_24(app, well):
    with app.test_request_context(
        method="POST", data=_form_data(well, operating_hours=24)
    ):
        form = CreateDailyProduction()
        assert form.validate()
        assert "operating_hours" not in form.errors


def test_accepts_operating_hours_valid_value(app, well):
    with app.test_request_context(
        method="POST", data=_form_data(well, operating_hours=20)
    ):
        form = CreateDailyProduction()
        assert form.validate()
        assert "operating_hours" not in form.errors


def test_rejects_nonexistent_well_id(app, well):
    with app.test_request_context(
        method="POST", data=_form_data(well_id=99999, operating_hours=20)
    ):
        form = CreateDailyProduction()
        assert not form.validate()
        assert "well_id" in form.errors


def test_rejects_duplicate_report_for_same_well_and_date(app, well):
    """Второй рапорт на ту же скважину и дату должен быть отклонен."""
    import datetime
    from app.extensions import db
    from app.models import DailyProduction

    with app.app_context():
        existing = DailyProduction(
            well_id=well,
            date=datetime.date(2026, 8, 3),
            operating_hours=10,
            liquid_produced=100,
            water_cut=10,
            density=800,
        )
        db.session.add(existing)
        db.session.commit()

    with app.test_request_context(
        method="POST", data=_form_data(well, date="2026-08-03", operating_hours=20)
    ):
        form = CreateDailyProduction()
        assert not form.validate()
        assert "date" in form.errors