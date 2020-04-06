from .blueprint import controller as queue
from app.helpers.mail import get_queue, get_queue_count
from flask.json import jsonify
import re
from config import mailServer


@queue.route('/')
def emails():
    stdout, stderr = get_queue()
    if mailServer == "exim":
        stdout = stdout.rstrip("\n")
        lines = stdout.splitlines()
        output = []
        for line in lines:
            if re.search('<', line) == None:
                continue
            line =line.strip()
            fields = line.split()
            payload = {}
            payload["queueTime"] = fields[0]
            payload["mailSize"] = fields[1]
            payload["messageId"] = fields[2]
            payload["toAddress"] = fields[3]
            payload["status"] = fields[5]
            output.append(payload)
        if stderr:
            return jsonify(code=1, message=stderr), 400
        else:
            return jsonify(code=0, message="OK", queue=output), 200
    elif mailServer == "postfix":
        stdout = stdout.rstrip("\n")
        lines = stdout.splitlines()
        output = []
        for line in lines:
            if re.search('@', line) == None:
                continue
            line =line.strip()
            fields = line.split()
            if len(fields) < 7:
                continue
            payload = {}
            payload["queueTime"] = fields[3] + " " + fields[4] + " " + fields[5]
            payload["mailSize"] = fields[1]
            payload["messageId"] = fields[0]
            payload["FromAddress"] = fields[6]
            payload["status"] = "queued"
            output.append(payload)
        return jsonify(code=0, message="OK", queue=output), 200
    else:
         raise Exception('unknown mail server')


@queue.route('/count')
def count():
    stdout, stderr = get_queue_count()
    if stderr:
        return jsonify(code=1, message=stderr), 400
    else:
        return jsonify(code=0, message="OK", count=int(stdout)), 200

@queue.route('/messageId/<messageId>', methods=['GET'])
def checkMessageId(messageId):
    stdout, stderr = get_queue()
    if mailServer == "exim":
        stdout = stdout.rstrip("\n")
        lines = stdout.splitlines()
        output = []
        for line in lines:
            if  re.search('<', line) == None:
                continue
            line =line.strip()
            fields = line.split()
            if fields[2] != messageId:
                continue
            payload = {}
            payload["queueTime"] = fields[0]
            payload["mailSize"] = fields[1]
            payload["messageId"] = fields[2]
            payload["toAddress"] = fields[3]
            payload["status"] = fields[5]
            output.append(payload)
        if stderr:
            return jsonify(code=1, message=stderr), 400
        elif len(output) == 0:
            return jsonify(code=2, message="not found", queue=output), 404
        else:
            return jsonify(code=0, message="found", queue=output), 200
    elif mailServer == "postfix":
        stdout = stdout.rstrip("\n")
        lines = stdout.splitlines()
        output = []
        for line in lines:
            if re.search('@', line) == None:
                continue
            line =line.strip()
            fields = line.split()
            if fields[0] != messageId:
                continue
            payload = {}
            payload["queueTime"] = fields[3] + " " + fields[4] + " " + fields[5]
            payload["mailSize"] = fields[1]
            payload["messageId"] = fields[0]
            payload["fromAddress"] = fields[6]
            payload["status"] = "queued"
            output.append(payload)
        if stderr:
            return jsonify(code=1, message=stderr), 400
        elif len(output) == 0:
            return jsonify(code=2, message="not found", queue=output), 404
        else:
            return jsonify(code=0, message="found", queue=output), 200
    else:
        raise Exception('unknown mail server')
