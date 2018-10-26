from flask import Flask
from flask import render_template
import os

from flask import json
from flask import jsonify

application = Flask(__name__)

CONTAINER_NAME=os.uname()[1]

if 'APP_VERSION' in os.environ:
    CONTAINER_VERSION = os.environ['APP_VERSION']
else:
    CONTAINER_VERSION = "v1"

if 'APP_MESSAGE' in os.environ:
    CONTAINER_MESSAGE = os.environ['APP_MESSAGE']
else:
    CONTAINER_MESSAGE = ""

@application.route("/")
def index():
    return  render_template('index.html', container_name=CONTAINER_NAME, 
            container_version=CONTAINER_VERSION, container_message=CONTAINER_MESSAGE)

@application.route("/hello")
def hello():
    return "Hello from " + CONTAINER_NAME + " " + CONTAINER_VERSION

@application.route("/_healthz")
def status():
    return jsonify(status="OK",
                   container_name=CONTAINER_NAME,
                   container_version=CONTAINER_VERSION,
                   container_message=CONTAINER_MESSAGE)


@application.route("/_net")
def pod_ifaces():
    return jsonify(status="OK",
                   container_name=CONTAINER_NAME,
                   container_version=CONTAINER_VERSION,
                   interface_name='<not implemented>')

if __name__ == "__main__":
    application.run()
