from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
# from flask_sqlalchemy import sqlalchemy

app = Flask(__name__)

######
employees = [
    {
        "id" : 1,
        "name": "Александр Иванов",
        "email": "alexandr.ivanov@example.com",
        "position": "Менеджер по продажам",
    },
    {    
        "id" : 2,
        "name": "Елена Петрова",
        "email": "elena.petrova@example.com",
        "position": "Бухгалтер",
    },
    {
        "id" : 3,
        "name": "Дмитрий Смирнов",
        "email": "dmitry.smirnov@example.com",
        "position": "Системный администратор",
    },
    {
        "id" : 4,
        "name": "Анна Кузнецова",
        "email": "anna.kuznetsova@example.com",
        "position": "HR-специалист",
    },
    {
        "id" : 5,
        "name": "Михаил Попов",
        "email": "mikhail.popov@example.com",
        "position": "Программист",
    },
    {
        "id" : 6,
        "name": "Ольга Васильева",
        "email": "olga.vasilieva@example.com",
        "position": "Маркетолог",
    },
    {
        "id" : 7,
        "name": "Сергей Соколов",
        "email": "sergey.sokolov@example.com",
        "position": "Директор по развитию",
    },
    {
        "id" : 8,
        "name": "Татьяна Новикова",
        "email": "tatiana.novikova@example.com",
        "position": "Юрист",
    },
    {
        "id" : 9,
        "name": "Андрей Федоров",
        "email": "andrey.fedorov@example.com",
        "position": "Аналитик данных",
    },
    {
        "id" : 10,
        "name": "Мария Морозова",
        "email": "maria.morozova@example.com",
        "position": "Дизайнер интерфейсов",
    }
]
#####

@app.route('/')
def index():
    return render_template("main/index.html", employees=employees)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["excel_file"]

    df = pd.read_excel(file)
    employees = df.to_dict(orient="records")

    return render_template(
        "main/index.html",
        employees=employees
    )


@app.route("/create", methods=["GET", "POST"])
def create_employee():

    if request.method == "POST":
        try:
            employee = {
                "id": len(employees) + 1,
                "name": request.form["name"],
                "email": request.form["email"],
                "position": request.form["position"],
            }

            employees.append(employee)

            return redirect(url_for("index"))
        except Exception as e:
            return f"ERROR{e}"

    return render_template("main/create_employee.html")

@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete_employee(id:int):

    if request.method == "POST":
        try:
            for employee in employees:
                if employee["id"] == id:
                    employees.remove(employee)
                    break
            return redirect(url_for("index"))
        except Exception as e:
            return f"ERROR {e}"
    

# class DataRow(db.Model):
#     id = db.Column(db.Integer, primary_key = True)

if __name__ == '__main__':
    app.run(debug=True)