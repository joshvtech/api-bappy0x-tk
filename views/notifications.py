from flask import Blueprint, request, jsonify, abort

from .docs import auto_docs

from sys import path
path.append("...")
from db.models import tblNotifications

from datetime import datetime

blueprint = Blueprint("notifications", __name__, url_prefix="/notifications")

@blueprint.route("/<int:id>", methods=["GET"])
@auto_docs.doc()
def from_id(id):
    """
        <h3>Get a Notification by its ID</h3>
        <p>Each notification has an ID - use this method to get it.</p>
        <h4>Response Notification Object Values:</h4>
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Type</th>
                    <th>Maximum Value</th>
                    <th>Example</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>id</td>
                    <td>integer</td>
                    <td>N/A</td>
                    <td><code>3</code></td>
                </tr>
                <tr>
                    <td>important</td>
                    <td>boolean</td>
                    <td>N/A</td>
                    <td><code>true</code></td>
                </tr>
                <tr>
                    <td>timestamp</td>
                    <td>datetime or null</td>
                    <td>N/A</td>
                    <td><code>"Sat, 09 May 2020 22:20:00 GMT"</code></td>
                </tr>
                <tr>
                    <td>head</td>
                    <td>string</td>
                    <td>128 Characters</td>
                    <td><code>"&lti class=\\"fas fa-tools\\"&gt&lt/i&gt This site is still under construction..."</code></td>
                </tr>
                <tr>
                    <td>body</td>
                    <td>string</td>
                    <td>512 Characters</td>
                    <td><code>"Please note that I am still building this site as you view it, this constantly gets updated and changed."</code></td>
                </tr>
            </tbody>
        </table>
        <br>
        <h4>Examples:</h4>
        <p>Raw URL:</p>
        <a href="{{ url_for('notifications.from_id', id=3) }}" target="_blank">https://{{ request.host }}{{ url_for("notifications.from_id", id=3) }} <i class="fas fa-external-link-alt align-text-top" style="font-size: 0.5rem"></i></a>
        <p>cURL Example:</p>
        <code>
            curl -X GET "https://{{ request.host }}/notifications/3"
        </code>
        <br>
        <p>Python Example:</p>
        <code>
            import requests<br>
            response = requests.get("https://{{ request.host }}/notifications/3")<br>
            print(response.json())<br>
        </code>
    """
    result = tblNotifications.query.get(id)
    if result is None:
        return abort(404)
    result = dict(result)
    success = True
    return jsonify(**locals())

@blueprint.route("/list", methods=["GET"])
@auto_docs.doc()
def list():
    """
        <h3>Get a Full List of Notifications</h3>
        <h4>Request URL Parameters:</h4>
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Type</th>
                    <th>Default</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
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
            </tbody>
        </table>
        <p>These are also stored in a "requestParams" object within the JSON response.</p>
        <br>
        <h4>Examples:</h4>
        <p>Raw URL:</p>
        <a href="{{ url_for('notifications.list') }}?valid=True&removeImportant=False&max=5" target="_blank">https://{{ request.host }}{{ url_for('notifications.list') }}?valid=True&removeImportant=False&max=5 <i class="fas fa-external-link-alt align-text-top" style="font-size: 0.5rem"></i></a>
        <p>cURL Example:</p>
        <code>
            curl -X GET "https://{{ request.host }}/notifications/list" -d valid=True -d removeImportant=False -d max=5
        </code>
        <br>
        <p>Python Example:</p>
        <code>
            import requests<br>
            response = requests.get("https://{{ request.host }}/notifications/list", params={"valid": True, "removeImportant": False, "max": 3})<br>
            print(response.json())<br>
        </code>
    """
    #Define the request paramaters as a dict and query SQL for all notifications.
    requestParams = {
        "valid":           request.args.get("valid", default=True, type=bool),
        "removeImportant": request.args.get("removeImportant", default=False, type=bool),
        "max":             request.args.get("max", default=5, type=int)
    }
    notifs = tblNotifications.query.all()

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