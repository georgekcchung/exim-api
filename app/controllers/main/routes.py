from .blueprint import controller as main
from flask import jsonify


@main.route('/')
@main.route('/healthcheck')
def health():
    return jsonify(code=0, message='OK'), 200
#    return 'OK', 200
