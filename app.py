from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as db
from sqlalchemy.sql import select, exists
from datetime import datetime

from sqlalchemy.sql.expression import false, true

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


###############################################
## Database Initialization
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_last_name = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(200), nullable = False)
    address = db.Column(db.String(200), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    job_title= db.Column(db.String(200), nullable = False)
    salary= db.Column(db.Integer, nullable = False)
    password = db.Column(db.String(200),nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __init__(self,first_last_name,username,email,address,age,job_title,salary,password):
        self.first_last_name = first_last_name
        self.username = username
        self.email = email
        self.address = address
        self.age = age
        self.job_title = job_title
        self.salary = salary
        self.password = password
            
# Function to return string when new data is added
    def __repr__(self):
        return '<name %r>' % self.id  


###############################################
## Login Route
@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        exists = false
        if (db.session.query(db.exists().where(Person.username == username)).scalar() and 
            db.session.query(db.exists().where(Person.password == password)).scalar()):
            exists = true 

        if exists == true:
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
        
    return render_template('login.html')


###############################################
## Signup Route
@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        new_first_last_name = request.form['first_last_name']
        new_username = request.form['username']
        new_email = request.form['email']
        new_address = request.form['address']
        new_age = request.form['age']
        new_job_title = request.form['job_title']
        new_salary = request.form['salary']
        new_password = request.form['password']

        user = Person(new_first_last_name,new_username,new_email,new_address,new_age,new_job_title, new_salary,new_password)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('login'))

    return render_template('signup.html')


###############################################
## Default Route
@app.route("/")
def home():
    return render_template('index.html')


###############################################
## General
if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
