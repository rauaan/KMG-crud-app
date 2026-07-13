import click 
from flask.cli import with_appcontext
from app.extensions import faker
# from models import Company

@click.command(name = 'make-data')
@with_appcontext
def make_data():
    print(faker.name())

    # for i in range(22):
    #     new_company = Company(
    #         name = faker.company.name(),
    #         region = request.form['region']
    #     )
