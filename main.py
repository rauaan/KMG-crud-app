from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main/index.html')

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["excel_file"]

    df = pd.read_excel(file)
    employees = df.to_dict(orient="records")

    return render_template(
        "main/index.html",
        employees=employees
    )

if __name__ == '__main__':
    app.run(debug=True)