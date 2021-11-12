from flask import Flask, render_template, request, redirect, url_for, session, app
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import select, exists
from sqlalchemy.sql.expression import false, true
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


import sqlalchemy as db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

db = SQLAlchemy(app)
Session(app)

###############################################
## Database Initialization

class Person(db.Model):
    id           = db.Column(db.Integer, primary_key = True)
    fullname     = db.Column(db.String(200), nullable = False)
    username     = db.Column(db.String(200), nullable = False)
    address      = db.Column(db.String(200), nullable = False)
    age          = db.Column(db.Integer)
    salary       = db.Column(db.Integer)
    job_title    = db.Column(db.String(200), nullable = False)
    password     = db.Column(db.String(200),nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)   

    #Throw exception if the password is not readable
    @property
    def password(self):
        raise AttributeError('Not a readable password!')

    #Hashes and salts user inputted password
    @password.setter
    def password(self,password):
        self.password = generate_password_hash(password)
 
    #verifies hashed password
    def verify_pass(self,password):
        return check_password_hash(self.password,password)

    
    def __init__(self,fullname,username,address,age,salary,job_title,password):
        self.fullname   = fullname
        self.username   = username
        self.address    = address
        self.age        = age
        self.salary     = salary
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
        new_fullname    = request.form['fullname']
        new_username    = request.form['username']
        new_address     = request.form['address']
        new_age         = request.form['age']
        new_salary      = request.form['salary']
        new_job_title   = request.form['job_title']
        new_password    = request.form['password']

        # Check all fields are filled out
        if (not new_fullname  or not new_username  or not new_address   or not new_age
            or not new_salary or not new_job_title or not new_password):
            return render_template('signup.html', error = False)

        # Check if username already exists
        if db.session.query(db.exists().where(Person.username == new_username)).scalar():
            return render_template('signup.html', duplicate = True)

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
## General
if __name__ == "__main__":
    # db.create_all()
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
