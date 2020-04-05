from flask import request, jsonify

from .blueprint import controller as check
from app.helpers.exim import check_delivery_route
import re


@check.route('/route/', methods=['POST'])
def delivery_route():
    json = request.get_json()
    email = json.get('email', '').strip()
    if not email:
        return jsonify(error='Email is required'), 422

    stdout, stderr = check_delivery_route(email)

    if stderr != "":
        return jsonify(code=2, message='internal error'), 500

    if 'host lookup did not complete' in stdout:
        return jsonify(code=1, message='Host cannot be resolved'), 404

    if re.search("remote_smtp", stdout) == None: 
        return jsonify(code=1, message='not routable'), 404

    return jsonify(code=0, message='found routable')
