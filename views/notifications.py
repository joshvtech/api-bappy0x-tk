from flask import Blueprint, request, jsonify

from .docs import auto_docs

from sys import path
path.append("...")
from db.models import notifications

from datetime import datetime

blueprint = Blueprint("notifications", __name__, url_prefix="/notifications")

@blueprint.route("/<int:id>", methods=["GET"])
@auto_docs.doc()
def from_id(id):
    return jsonify(success=id)

@blueprint.route("/list", methods=["GET"])
@auto_docs.doc()
def list():
    """
Get a List of Notifications
=================

> this is a codeblock

this is an _em_.

Form data: test

URL Params:

valid, boolean, defaults to true -- filter out notifications that are ahead of the current time

removeImportant, boolean, defaults to false -- remove notifications that are important

max, integer, defaults to 5 -- the amount of notifications to be returned

Will also return a requestParams dict with parameters used.

```
this is code
```
    """
    #Define the request paramaters as a dict and query SQL for all notifications.
    requestParams = {
        "valid":            request.args.get("valid", default=True, type=bool),
        "removeImportant":  request.args.get("removeImportant", default=False, type=bool),
        "maximum":          request.args.get("max", default=5, type=int)
    }
    notifs = notifications.query.all()

    #Filter depending on params
    if requestParams["valid"]:
        notifs = [i for i in notifs if (i.timestamp == None) or (i.timestamp < datetime.now())]
    if requestParams["removeImportant"]:
        notifs = [i for i in notifs if not i.important]
    notifs = notifs[:requestParams["maximum"]]

    #Convert notifs to dicts, set success to true and return response
    notifs = [dict(i) for i in notifs]
    success = True
    return jsonify(**locals())