from flask import Request
import functions_framework
import json

from event_detector import run

@functions_framework.http
def event_detector(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'pattern' in request_json:
        pattern = request_json['pattern']
    elif request_args and 'pattern' in request_args:
        pattern = request_args['pattern']
    else:
        pattern = "A(.*).gz"

    run(pattern)
    return 'OK'

if __name__ == "__main__":
    request = Request({})
    request.data = json.dumps({"pattern": "A(.*).gz"})
    event_detector(request)