from flask import jsonify
from datetime import datetime

def _str(val):
    """
    Ensures that the val is the default str() type for python2 or 3
    """
    if str == bytes:
        if isinstance(val, str):
            return val
        else:
            return str(val)
    else:
        if isinstance(val, str):
            return val
        else:
            return str(val, 'ascii')

# -------- Error response functions -----


def permissionDenied():
    return jsonify({
        "status": "error",
        "msg": "User is not logged in."
    }), 401


def missingData():
    return jsonify({
        "status": "error",
        "msg": "Necessary data is missing."
    }), 400


def badUser():
    return jsonify({
        "status": "error",
        "msg": "You are not admin of this contest."
    }), 400


def somethingWrong():
    return jsonify({
        "status": "error",
        "msg": "Something went wrong."
    }), 400


def defaultRules():
    return {
        "namespaceMain": False,
        "creationInRange": False,
        "authorOnly": False,
        "submitterRegDate": {
            "status": False,
            "value": datetime.today().strftime('%Y-%m')
        },
        "pageSize": {
            "status": False,
            "mode": "bytes",
            "bytes": None,
            "words": None
        },
        "pageSizeBySubmitter": {
            "status": False,
            "mode": "bytes",
            "bytes": None
        },
        "minImages": {
            "status": False,
            "value": None
        },
        "minTemplates": {
            "status": False,
            "value": None
        },
        "minCategories": {
            "status": False,
            "value": None
        },
        "minLangLinks": {
            "status": False,
            "value": None
        }
    }
