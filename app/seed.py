"""Команда Flask CLI для автоматического заполнения базы данных тестовыми данными.

Модуль генерирует реалистичные данные для нефтяных компаний, сотрудников,
скважин и суточных производственных рапортов с использованием библиотеки Faker.
Используется для разработки, тестирования и демонстрации работы системы.
"""

import click 
import random
from datetime import date, timedelta
from flask.cli import with_appcontext
from app.extensions import faker, db
from app.models import Company, Well, User, DailyProduction

today = date.today()

@click.command(name = 'make-data')
@with_appcontext
def make_data():
    """Заполняет базу данных тестовыми данными.

    Перед генерацией очищает существующие записи в таблицах сотрудников,
    скважин, компаний и суточных рапортов.

    После очистки создаются:
        - 22 нефтяные компании;
        - от 2 до 5 сотрудников для каждой компании;
        - от 2 до 10 скважин для каждой компании;
        - суточные производственные рапорты за последние 365 дней
          для случайных 2–5 компаний.

    Все созданные объекты сохраняются в базе данных одной командой
    для каждой сущности.
    """

    companies = []
    wells = []
    users = []
    daily_productions = []

    User.query.delete()
    DailyProduction.query.delete()
    Well.query.delete()
    Company.query.delete()


    db.session.commit()

    for _ in range(22):
        new_company = Company(
            name = faker.company(),
            region = faker.city()
        )
        companies.append(new_company)
    
    for company in companies:
        for _ in range(random.randint(2, 10)):
            wells.append(
                Well(
                name=faker.word(),
                type=faker.random_element(["Oil", "Gas"]),
                max_drilling_depth=random.randint(1000, 5000),
                company=company
            ))

    for company in companies:
        for _ in range(random.randint(2, 5)):
            users.append(
                User(
                lName=faker.last_name(),
                fName=faker.first_name(),
                company=company
            ))
    
    for company in companies[:random.randint(2, 5)]:
        
        a_well = company.wells[random.randint(0,len(company.wells)-1)]

        for i in range(365):

            report_date = today - timedelta(days=i)
            

            daily_productions.append(
                DailyProduction(
                    well = a_well,
                    date=report_date,
                    operating_hours = random.randint(0, 24),
                    liquid_produced = random.randint(800, 1200),
                    water_cut = random.randint(0, 100),
                    density = random.randint(800, 1200)
                    )
            )


    try:
        db.session.add_all(companies)
        db.session.commit()
        db.session.add_all(users)
        db.session.commit()
        db.session.add_all(wells)
        db.session.commit()
        db.session.add_all(daily_productions)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print (f"Ошибка генерации данных: {e}")
