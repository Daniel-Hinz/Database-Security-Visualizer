from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)


###############################################
## Login Route
@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('home'))
        
    return render_template('login.html')


###############################################
## Signup Route
@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
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