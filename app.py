from flask import Flask, render_template
app = Flask(__name__)


###############################################
## Default Route
@app.route("/")
def main():
    return render_template('index.html')


###############################################
## Signup Route
@app.route("/signup")
def signup():
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