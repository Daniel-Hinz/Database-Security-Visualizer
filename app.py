from flask import Flask, render_template, request, redirect, url_for, session, app
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import defer
from werkzeug.security import generate_password_hash, check_password_hash

import sqlalchemy as db
import re

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
## Login Route
@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']

        user = Person.query.filter_by(username = username).first()

        if not user:
            return render_template('login.html', loginFailed = True)

        if user.password == password:
        # if check_password_hash(user.password, password):
            session["name"] = request.form.get("username")
            return redirect(url_for('home'))
         
        return render_template('login.html', loginFailed = True)
        
    return render_template('login.html')


###############################################
## Default Route
@app.route("/")
def home():
    if not session.get("name"):
        return redirect(url_for("login"))
    
    return render_template('index.html', headings = Person.__table__.columns.keys(), people = Person.query.all())


###############################################
## Populate Database
@app.route("/populate")
def populate():
    with open('dummy.txt', 'r') as file:
        for line in file:
            values = re.split(r'\t+', line.rstrip('\t'))
            values[6] = values[6][:len(values[6])-1]
            
            if not db.session.query(db.exists().where(Person.username == values[1])).scalar():
                user = Person(values[0], values[1], values[2], values[3], values[4], values[5], values[6])
                db.session.add(user)
        
        db.session.commit() 

    return render_template('index.html', headings = Person.__table__.columns.keys(), people = Person.query.all())


###############################################
## Hash Password
@app.route("/hash")
def hash():
    for person in Person.query.all():
        person.password = generate_password_hash(person.password, method='pbkdf2:sha256', salt_length=16)

    db.session.commit()
    return render_template('index.html', headings = Person.__table__.columns.keys(), people = Person.query.all())


###############################################
## Anonymize
@app.route("/anonymize", methods = ['GET', 'POST'])
def anonymize():
    for person in Person.query.all():

        # Hide username and password
        defer(person.username)
        defer(person.password)

        # Replace all names with "*"
        person.fullname = "*"

        # Limit address to the first 3 digits of the zip
        person.address = person.address[len(person.address)-6:len(person.address)-2] 

        # Make the ages either > 45 or <= 45
        person.age = "> 45" if int(person.age) > 45 else "<= 45"

        # Make the salary either > 45k or <= 45k 
        person.salary = "> 45" if int(person.salary) > 45000 else "<= 45"
    
    db.session.commit()
    return render_template('index.html', headings = Person.__table__.columns.keys(), people = Person.query.with_entities(Person.id, Person.fullname, Person.address, Person.age, Person.salary, Person.job_title))

###############################################
## Reset Table
@app.route("/reset")
def reset():
    Person.__table__.drop(db.engine)
    db.create_all()
    session.clear()
    return redirect(url_for("login"))


###############################################
## Signout Route
@app.route("/signout", methods = ['GET', 'POST'])
def signout():
    session.clear()
    return redirect(url_for("login"))


###############################################
## General
if __name__ == "__main__":
    db.create_all()
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
