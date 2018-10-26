from flask import Flask
from flask import render_template
import os

from flask import json
from flask import jsonify

import netifaces

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
    netiflist=netifaces.interfaces()
    first_inet_if = netiflist[0]
    try:
        first_inet = netifaces.ifaddresses(first_inet_if)[netifaces.AF_INET]
    except:
        first_inet = first_inet_if + " Does not contains valid IPv4"
    return jsonify(status="OK",
                   container_name=CONTAINER_NAME,
                   container_version=CONTAINER_VERSION,
                   interface_list=netiflist,
                   first_inet=first_inet)

if __name__ == "__main__":
    application.run()
