from flask import Blueprint, request, jsonify, abort

from .docs import auto_docs

from os import getenv
from requests import post
#from datetime import datetime

blueprint = Blueprint("jetradio", __name__, url_prefix="/jetradio")

@blueprint.route("/request", methods=["POST"])
@auto_docs.doc()
def listener_request():
    """
        <h3>Send a Listener Request to Jet Radio</h3>
        <p>Passes given data through validation and then passes it to Discord to show to presenters and etc.</p>
        <h4>JSON Values:</h4>
        <table>
            <tr>
                <td>Key</td>
                <td>Value Type</td>
                <td>Maximum Value</td>
                <td>Example</td>
            </tr>
            <tr>
                <td>type</td>
                <td>string</td>
                <td>["shoutout", "play"]</td>
                <td><code>""</code></td>
            </tr>
            <tr>
                <td>name</td>
                <td>string</td>
                <td>N/A</td>
                <td><code>"Josh"</code></td>
            </tr>
            <tr>
                <td>message</td>
                <td>string</td>
                <td>N/A</td>
                <td><code>"Hello! I'm on the M6 cruising, quite sweet."</code></td>
            </tr>
        </table>
        <br>
        <h4>Examples:</h4>
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
        "avatar_url": "https://file.coffee/u/cRaSt2kar.png"
    }
    resp = post(getenv(f"{request_type.upper()}S_URL"), json=discord_json)
    if resp.status_code in range(200, 299):
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})