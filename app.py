from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employees.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your_secret_key"

db = SQLAlchemy(app)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)


@app.route("/")
def index():
    """this renders the index page when its called"""
    employees = Employee.query.all()
    return render_template("index.html", employees=employees)


@app.route("/add", methods=["POST", "GET"])
def add_employee():
    """here, i wrote a functino for adding new employees"""
    if request.method == "POST":
        username = request.form["username"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        role = request.form["role"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)

        new_employee = Employee(
            username=username,
            first_name=first_name,
            last_name=last_name,
            role=role,
            password=hashed_password,
        )
        db.session.add(new_employee)
        db.session.commit()
        flash("Employee added successfully!")
        return redirect(url_for("index"))

    return render_template("add_employee.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    if request.method == "POST":
        employee.username = request.form["username"]
        employee.first_name = request.form["first_name"]
        employee.last_name = request.form["last_name"]
        employee.role = request.form["role"]
        if request.form["password"]:  # Only update password if field is not empty
            employee.password = generate_password_hash(request.form["password"])
        db.session.commit()
        flash("Employee updated successfully!")
        return redirect(url_for("index"))

    return render_template("edit_employee.html", employee=employee)


@app.route("/delete/<int:id>")
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash("Employee deleted successfully!")
    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
