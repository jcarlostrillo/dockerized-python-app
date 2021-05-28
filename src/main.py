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

    # persist exam
    session = Session()
    session.add(request_candidate)
    session.commit()

    # return created exam
    crated_request = RequestSchema().dump(request_candidate)
    session.close()
    return jsonify(crated_request), 201

@app.route("/")
def index():
    ip_address = request.remote_addr
    path = request.path
    hostname_container = socket.gethostname()
    now = datetime.now()
    time = now.strftime("%m/%d/%Y, %H:%M:%S")

    writeToFile(ip_address, path, hostname_container, time)

   
    conn = postgress_connection()
    conn.insert(ip_address, path, hostname_container, time)
    records = conn.selectAll()
    conn.close()
    return jsonify(records)

@app.route("/hi")
def who():
    return "Who are you?"

@app.route("/hi/<username>")
def greet(username):
    return f"Hi there, {username}!"

def writeToFile(ip_address, path, hostname_container, time):
    f = open("/tmp/requests.txt", "a")
    f.write("IP Adress: " + ip_address + "\n")
    f.write("PATH: " + path  + "\n")
    f.write("Hostname: " + hostname_container + "\n")
    f.write("Time: " + time + "\n")
    f.write("--------------------------------------------------\n")
    f.close()

