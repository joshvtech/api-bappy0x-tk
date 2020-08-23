from flask import Blueprint, request, jsonify, abort

from .docs import auto_docs
from os import getenv

from sys import path
path.append("...")
from db.models import jetradio_events as events

from requests import post
from datetime import datetime, timezone

blueprint = Blueprint("jetradio", __name__, url_prefix="/jetradio")

@blueprint.route("/request", methods=["POST"])
@auto_docs.doc()
def listener_request():
    """
        <h3>Send a Listener Request to Jet Radio</h3>
        <p>Passes given data through validation and then passes it to Discord to show to presenters and etc.</p>
        <h4>Request JSON Values:</h4>
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Key</th>
                    <th>Value Type</th>
                    <th>Example</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>type</td>
                    <td>string</td>
                    <td><code>"shoutout"/"play"</code></td>
                </tr>
                <tr>
                    <td>name</td>
                    <td>string</td>
                    <td><code>"Josh"</code></td>
                </tr>
                <tr>
                    <td>message</td>
                    <td>string</td>
                    <td><code>"Hello! I'm on the M6 cruising, quite sweet."</code></td>
                </tr>
            </tbody>
        </table>
        <br>
        <h4>Examples:</h4>
        <p>Make sure to include the "Content-Type" Header.</p>
        <p>cURL Example:</p>
        <code>
            curl -X POST "https://{{ request.host }}/jetradio/request" -H "Content-Type: application/json" -d '{"type": "shoutout", "name": "Josh", "message": "Hello! I\\u0027m on the M6 cruising, quite sweet."}'
        </code>
        <br>
        <p>Python Example:</p>
        <code>
            import requests<br>
            response = requests.post("https://{{ request.host }}/jetradio/request", json={"type": "shoutout", "name": "Josh", "message": "Hello! I'm on the M6 cruising, quite sweet."})<br>
            print(response.json())<br>
        </code>
    """
    if not request.json:
        return jsonify({"success": False, "error": "Missing JSON Data"})

    request_types = {"shoutout": 15818848, "play": 16043833}
    request_type = request.json.get("type")
    request_name = request.json.get("name")
    request_message = request.json.get("message")

    if not(request_type and request_name and request_message):
        return jsonify({"success": False, "error": "Missing Required Data"})
    if not request_type in request_types:
        return jsonify({"success": False, "error": "Incorrect Type Data"})

    discord_json = {
        "embeds": [
            {
                "title": f":exclamation: New {request_type.title()} Request",
                "color": request_types[request_type],
                "fields": [
                    {
                        "name": "> **Name**",
                        "value": f"```\n{request_name}```"
                    },
                    {
                        "name": "> **Message**",
                        "value": f"```\n{request_message}```"
                    }
                ],
                "footer": {
                    "text": f"Recieved from `{request.remote_addr}` via `{request.headers.get('User-Agent')}`"
                }
            }
        ],
        "username": "jetradio.live",
        "avatar_url": "https://jetradio.live/public/img/Logo.png"
    }
    resp = post(getenv(f"{request_type.upper()}S_URL"), json=discord_json)
    if resp.status_code in range(200, 299):
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})


@blueprint.route("/currentevent", methods=["GET"])
@auto_docs.doc()
def current_event():
    """
        <h3>Get The Current Jet Radio Event</h3>
        <p>Passes given data through validation and then passes it to Discord to show to presenters and etc.</p>
        <h4>Response Event Object JSON Values:</h4>
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Key</th>
                    <th>Value Type</th>
                    <th>Maximum Value</th>
                    <th>Example</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>id</td>
                    <td>integer</td>
                    <td>N/A</td>
                    <td><code>1</code></td>
                </tr>
                <tr>
                    <td>name</td>
                    <td>string</td>
                    <td>128 Characters</td>
                    <td><code>"Josh"</code></td>
                </tr>
                <tr>
                    <td>image</td>
                    <td>string</td>
                    <td>128 Characters</td>
                    <td><code>"https://jetradio.live/public/img/presenters/Josh.jpg"</code></td>
                </tr>
                    <td>feature</td>
                    <td>string</td>
                    <td>128 Characters</td>
                    <td><code>"The Ultimate Party Hits"</code></td>
                </tr>
                    <td>timeStart</td>
                    <td>datetime w/timezone</td>
                    <td>N/A</td>
                    <td><code>Sun, 23 Aug 2020 19:00:00 GMT</code></td>
                </tr>
                    <td>timEnd</td>
                    <td>datetime w/timezone</td>
                    <td>N/A</td>
                    <td><code>Sun, 23 Aug 2020 19:45:00 GMT</code></td>
                </tr>
            </tbody>
        </table>
        <p>"timeNow" and "success" are also returned within the JSON response.</p>
        <br>
        <h4>Examples:</h4>
        <p>cURL Example:</p>
        <code>
            curl -X GET "https://{{ request.host }}/jetradio/currentevent"
        </code>
        <br>
        <p>Python Example:</p>
        <code>
            import requests<br>
            response = requests.get("https://{{ request.host }}/jetradio/currentevent")<br>
            print(response.json())<br>
        </code>
    """
    timeNow = datetime.utcnow().replace(tzinfo=timezone.utc)
    active = [i for i in events.query.all() if i.timeStart <= timeNow and i.timeEnd > timeNow]
    event = None
    if len(active) > 0: event = dict(active[0])
    del active
    success = True
    return jsonify(**locals())