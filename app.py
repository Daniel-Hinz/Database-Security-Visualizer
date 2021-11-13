from flask import Flask, render_template, request, redirect, url_for, session, app
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Text
from sqlalchemy.orm import deferred
from sqlalchemy.sql.expression import false, true
from datetime import datetime

import sqlalchemy as db
import math, re

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

db = SQLAlchemy(app)
Session(app)

###############################################
## Database Initialization

class Person(db.Model):
    id           = db.Column(db.Integer,  primary_key = True)
    fullname     = db.Column(db.String(200), nullable = True)
    username     = db.Column(db.String(200), nullable = True)
    address      = db.Column(db.String(200), nullable = True)
    age          = db.Column(db.String(200), nullable = True)
    salary       = db.Column(db.String(200), nullable = True)
    job_title    = db.Column(db.String(200), nullable = True)
    password     = db.Column(db.String(200), nullable = True)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)    

    def __init__(self,fullname,username,address,age,salary,job_title,password):
        self.fullname   = "*"
        self.username   = username
        self.address    = address[len(address)-6:len(address)-2]
        self.age        = "> 45" if int(age) > 45 else "<= 45"
        self.salary     = str(math.floor(int(salary) / 10000) * 10000) + " - " + str((math.floor(int(salary) / 10000) + 1) * 10000)
        self.job_title  = job_title
        self.password   = password
            
    # Function to return string when new data is added
    def __repr__(self):
        return '<name %r>' % self.id  


###############################################
## Login Route
@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        session["name"] = request.form.get("username")

        username = request.form['username']
        password = request.form['password']

        exists = false
        if (db.session.query(db.exists().where(Person.username == username)).scalar() and 
            db.session.query(db.exists().where(Person.password == password)).scalar()):
            exists = true 

        if exists == true:
            return redirect(url_for('home'))
        else:
            return render_template('login.html', loginFailed = true)
        
    return render_template('login.html')


###############################################
## Signup Route
@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        new_fullname  = request.form['fullname']
        new_username  = request.form['username']
        new_address   = request.form['address']
        new_age       = request.form['age']
        new_salary    = request.form['salary']
        new_job_title = request.form['job_title']
        new_password  = request.form['password']

        # Check all fields are filled out
        if (not new_fullname  or not new_username  or not new_address   or not new_age
            or not new_salary or not new_job_title or not new_password):
            return render_template('signup.html', error = False)

        # Check if username already exists
        if db.session.query(db.exists().where(Person.username == new_username)).scalar():
            return render_template('signup.html', duplicate = True)

        # Add user to database
        user = Person(new_fullname, new_username, new_address, new_age, new_salary, new_job_title, new_password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html')


###############################################
## Signout Route
@app.route("/signout", methods = ['GET', 'POST'])
def signout():
    session.clear()
    return redirect(url_for("login"))


###############################################
## Default Route
@app.route("/")
def home():
    if not session.get("name"):
        return redirect(url_for("login"))
    
    return render_template('index.html', 
                            headings = Person.__table__.columns.keys(), 
                            people   = Person.query.all())


###############################################
## Populate Database
def populate():
    with open('dummy.txt', 'r') as file:
        for line in file:
            values = re.split(r'\t+', line.rstrip('\t'))
            values[6] = values[6][:len(values[6])-1]
            user = Person(values[0], values[1], values[2], values[3], values[4], values[5], values[6])
            db.session.add(user)
        
        db.session.commit()            


###############################################
## General
if __name__ == "__main__":
    # db.create_all()
    # populate()
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
