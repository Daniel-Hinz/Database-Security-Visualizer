from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


###############################################
## Default Route
@app.route("/", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('home'))
        
    return render_template('index.html')


###############################################
## Signup Route
@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return redirect(url_for('login'))

    return render_template('signup.html')


###############################################
## Home Route
@app.route("/home")
def home():
    return render_template('home.html')


###############################################
## General
if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')