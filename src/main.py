from flask import Flask, jsonify
from flask import render_template
from flask import request
from datetime import datetime
from postgress_connection import postgress_connection
from flask_cors import CORS

from .entities.entity import Session, engine, Base
from .entities.request import Request, RequestSchema

import socket
import sys
import time

# Create the Flask app
app = Flask(__name__)
CORS(app)

@app.route('/requests')
def get_requests():
    # Start session
    session = Session()

    # Check for existing data
    requests_objects = session.query(Request).all()

    # Transforming into JSON-serializable objects
    schema = RequestSchema(many=True)
    requests = schema.dump(requests_objects)

    for request in requests:
        print(request)


    # Serializing as JSON
    session.close()
    return jsonify(requests)

@app.route('/requests/create') # , methods=['POST'])
def add_request():    
    request_candidate = Request(request.remote_addr, request.path, socket.gethostname(), datetime.now())

    # Persist request
    session = Session()
    session.add(request_candidate)
    session.commit()

    # Return created exam
    crated_request = RequestSchema().dump(request_candidate)
    session.close()
    return jsonify(crated_request), 201

@app.route("/requests/file")
def index():
    request_candidate = Request(request.remote_addr, request.path, socket.gethostname(), datetime.now())

    # Persist in a file
    writeToFile(request_candidate.ip, request_candidate.path, request_candidate.host, request_candidate.requested_at)
 
    return render_template("index.html", **locals())

def writeToFile(ip_address, path, hostname_container, time):
    f = open("/tmp/requests.txt", "a")
    f.write("IP Adress: " + ip_address + "\n")
    f.write("PATH: " + path  + "\n")
    f.write("Hostname: " + hostname_container + "\n")
    f.write("Time: " + str(time) + "\n")
    f.write("--------------------------------------------------\n")
    f.close()

