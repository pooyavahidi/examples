import datetime
import logging
import socket
import json
import os
from flask import Flask, Response, Blueprint, config, request
from werkzeug.exceptions import BadRequest

# api resources
from api.processes import processes_resource

# Environment variables
custom_label = os.environ.get("CUSTOM_LABEL")

# Setup the logging
log = logging.getLogger()
logging.basicConfig(
    format=(
        "[%(asctime)s] %(module)s.%(funcName)s() "
        "[%(levelname)s] %(message)s"
    ),
    level=logging.INFO,
)

# Run the flask app
app = Flask(__name__)

# register the resources
app.register_blueprint(processes_resource)


@app.errorhandler(BadRequest)
def handle_bad_requests(e):
    # Start with the correct headers and status code from the error
    response = e.get_response()
    # Replace the body with JSON
    response.data = json.dumps(
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response


@app.before_request
def before_request():
    log.info(request)


@app.route("/")
def index():
    ip = socket.gethostbyname(socket.gethostname())
    now = datetime.datetime.now()
    resp = {
        "receivedAt": str(now),
        "localIp": ip,
        "custom_label": custom_label,
    }
    return json.dumps(resp)


@app.route("/health")
def health():
    return Response(response="healthy", status=200)
