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
<h3>Get a List of Notifications</h3>

<table>
    <tr>
        <td>Name</td>
        <td>Type</td>
        <td>Default</td>
        <td>Description</td>
    </tr>
    <tr>
        <td>valid</td>
        <td>boolean</td>
        <td>true</td>
        <td>Filter out notifications that are ahead of the current time.</td>
    </tr>
    <tr>
        <td>removeImportant</td>
        <td>boolean</td>
        <td>False</td>
        <td>Remove notifications that are important.</td>
    </tr>
    <tr>
        <td>max</td>
        <td>integer</td>
        <td>5</td>
        <td>The amount of notifications to be returned.</td>
    </tr>
</table>
<br>
<p>cURL Example:</p>

<code>
    curl -X GET "https://api.bappy0x.tk/notifications/list" -d valid=True -d removeImportant=False -d max=5
</code>
<br>

<p>Python Example:</p>

<code>
    import requests<br>
    response = requests.get("http://localhost/notifications/list", params={"valid": True, "removeImportant": False, "max": 3})<br>
    print(response.json())<br>
</code>
    """
    #Define the request paramaters as a dict and query SQL for all notifications.
    requestParams = {
        "valid":           request.args.get("valid", default=True, type=bool),
        "removeImportant": request.args.get("removeImportant", default=False, type=bool),
        "max":             request.args.get("max", default=5, type=int)
    }
    notifs = notifications.query.all()

    #Filter depending on params
    if requestParams["valid"]:
        notifs = [i for i in notifs if (i.timestamp == None) or (i.timestamp < datetime.now())]
    if requestParams["removeImportant"]:
        notifs = [i for i in notifs if not i.important]
    notifs = notifs[:requestParams["max"]]

    #Convert notifs to dicts, set success to true and return response
    notifs = [dict(i) for i in notifs]
    success = True
    return jsonify(**locals())