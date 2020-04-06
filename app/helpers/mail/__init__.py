from ..process import Process
from config import mailServer, EXIM, POSTFIX, DIG
import re


def _call(command):
    try:
        return Process(command).communicate()
    except FileNotFoundError as e:
        return '', str(e)


def get_queue():
    if mailServer == "exim":
        return _call([EXIM, '-bp'])
    elif mailServer == "postfix":
        return _call([POSTFIX, '-bp'])
    else:
        raise Exception('unknown mail server')


def get_queue_count():
    if mailServer == "exim":
        return _call([EXIM, '-bpc'])
    elif mailServer == "postfix":
        mailQueue, tmp = _call([POSTFIX, '-bp'])
        mailQueue = mailQueue.rstrip("\n")
        lines = mailQueue.splitlines()
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
            payload["fromAddress"] = fields[6]
            payload["status"] = "queued"
            output.append(payload)
        return len(output), ""
    else:
        raise Exception('unknown mail server')


def check_delivery_route(email):
    if mailServer == "exim":
        return _call([EXIM, '-bt', email])
    else:
        tmp = email.split('@')
        if len(tmp) != 2:
            return "", "not valid mail"
        return _call([DIG, tmp[1], "mx"])
