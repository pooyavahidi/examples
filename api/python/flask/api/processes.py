import os
import time
import logging
import subprocess
from flask import Blueprint, request, Response
from werkzeug.exceptions import BadRequest

log = logging.getLogger()

processes_resource = Blueprint("processes_resource", __name__)


@processes_resource.route("/processes", methods=["POST"])
def post_process():
    req = request.get_json()
    timeout = req.get("timeout")
    args = req.get("args")
    if not args:
        raise BadRequest("args is empty")

    try:
        result = subprocess.run(
            args=args,
            check=True,
            env=os.environ.copy(),
            capture_output=True,
            encoding="utf-8",
            timeout=timeout,
        )

        log.info(result)
        return build_response(result)
        # return Response(response=result, status=200)

    except Exception as e:
        return Response(response=e, status=500)


def build_response(result):
    if not result:
        return None
    res = {
        "args": result.args,
        "returncode": result.returncode,
        "stderr": result.stderr,
        "stdout": result.stdout,
    }
    return res
