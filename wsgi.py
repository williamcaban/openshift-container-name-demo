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


@application.route("/_net", defaults={'ifname':0})
@application.route("/_net/<ifname>")
def pod_ifaces(ifname):
    netiflist = netifaces.interfaces()

    if ifname in netiflist:
        # invoking route /_net/<ifname> with valid ifname
        try:
            ifname_addr = netifaces.ifaddresses(ifname)[netifaces.AF_INET]
        except:
            ifname_addr = ifname + " does not have a valid IPv4"

        return jsonify( container_name=CONTAINER_NAME,
                        container_version=CONTAINER_VERSION,
                        ifname_addr=ifname_addr)
    else:
        # invoking route /_net route or not a valid ifname
        return jsonify( container_name=CONTAINER_NAME,
                        container_version=CONTAINER_VERSION,
                        interface_list=netiflist)

if __name__ == "__main__":
    application.run()
