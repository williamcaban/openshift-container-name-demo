from flask import Flask
from flask import render_template
import os

application = Flask(__name__)

@application.route("/")
def index():
    return render_template('index.html',container_name=os.uname()[1])

@application.route("/hello")
def hello():
    return "Hello World! from " + os.uname()[1]

if __name__ == "__main__":
    application.run()
