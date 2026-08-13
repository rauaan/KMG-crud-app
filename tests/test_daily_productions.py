"""Функциональные (feature) тесты контроллера DailyProductionController.

Проверяют полный путь запроса: HTTP -> роутинг -> форма -> контроллер -> БД,
через реальный тестовый клиент, а не напрямую вызывая форму.
"""
import datetime

from app.extensions import db
from app.models import DailyProduction


def _payload(well_id, **overrides):
    """Формирует базовый набор данных формы с возможностью переопределения полей."""
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


def test_operating_hours_over_24_is_rejected(app, auth_client, well):
    """Рапорт с operating_hours > 24 не должен создавать запись в БД."""
    response = auth_client.post(
        "/daily_productions/create",
        data=_payload(well, operating_hours=25),
        follow_redirects=True,
    )
    assert response.status_code == 200

    with app.app_context():
        assert DailyProduction.query.count() == 0


def test_operating_hours_negative_is_rejected(app, auth_client, well):
    """Рапорт с отрицательным operating_hours не должен создавать запись в БД."""
    response = auth_client.post(
        "/daily_productions/create",
        data=_payload(well, operating_hours=-1),
        follow_redirects=True,
    )
    assert response.status_code == 200

    with app.app_context():
        assert DailyProduction.query.count() == 0


def test_operating_hours_lower_boundary_0_is_accepted(app, auth_client, well):
    """Нижняя граница диапазона (operating_hours = 0) должна быть принята."""
    response = auth_client.post(
        "/daily_productions/create",
        data=_payload(well, operating_hours=0, date="2026-08-01"),
        follow_redirects=True,
    )
    assert response.status_code == 200

    with app.app_context():
        record = DailyProduction.query.filter_by(
            well_id=well, date=datetime.date(2026, 8, 1)
        ).first()
        assert record is not None
        assert record.operating_hours == 0


def test_operating_hours_upper_boundary_24_is_accepted(app, auth_client, well):
    """Верхняя граница диапазона (operating_hours = 24) должна быть принята."""
    response = auth_client.post(
        "/daily_productions/create",
        data=_payload(well, operating_hours=24, date="2026-08-02"),
        follow_redirects=True,
    )
    assert response.status_code == 200

    with app.app_context():
        record = DailyProduction.query.filter_by(
            well_id=well, date=datetime.date(2026, 8, 2)
        ).first()
        assert record is not None
        assert record.operating_hours == 24


def test_valid_operating_hours_creates_record(app, auth_client, well):
    """Корректный рапорт должен создать запись со всеми переданными полями."""
    response = auth_client.post(
        "/daily_productions/create",
        data=_payload(well, operating_hours=20, date="2026-08-03"),
        follow_redirects=True,
    )
    assert response.status_code == 200

    with app.app_context():
        record = DailyProduction.query.filter_by(
            well_id=well, date=datetime.date(2026, 8, 3)
        ).first()
        assert record is not None
        assert record.operating_hours == 20
        assert record.liquid_produced == 500
        assert record.water_cut == 20
        assert record.density == 800


def test_nonexistent_well_id_is_rejected(app, auth_client, well):
    """Рапорт со ссылкой на несуществующую скважину не должен создавать запись."""
    response = auth_client.post(
        "/daily_productions/create",
        data=_payload(well_id=99999, date="2026-08-04"),
        follow_redirects=True,
    )
    assert response.status_code == 200

    with app.app_context():
        assert DailyProduction.query.count() == 0


def test_duplicate_report_for_same_well_and_date_is_rejected(app, auth_client, well):
    """Повторный рапорт на ту же скважину и дату не должен создавать вторую запись
    и не должен перезаписывать существующую.
    """
    with app.app_context():
        existing = DailyProduction(
            well_id=well,
            date=datetime.date(2026, 8, 5),
            operating_hours=10,
            liquid_produced=100,
            water_cut=10,
            density=800,
        )
        db.session.add(existing)
        db.session.commit()

    response = auth_client.post(
        "/daily_productions/create",
        data=_payload(well, date="2026-08-05", operating_hours=20),
        follow_redirects=True,
    )
    assert response.status_code == 200

    with app.app_context():
        records = DailyProduction.query.filter_by(
            well_id=well, date=datetime.date(2026, 8, 5)
        ).all()
        assert len(records) == 1
        assert records[0].operating_hours == 10


def test_create_requires_authentication(client, well):
    """Неавторизованный пользователь должен быть перенаправлен, а не создать запись."""
    response = client.post(
        "/daily_productions/create",
        data=_payload(well),
        follow_redirects=False,
    )
    assert response.status_code in (302, 401, 403)