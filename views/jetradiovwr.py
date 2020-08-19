from flask import Blueprint, request, jsonify, abort

from .docs import auto_docs

from os import getenv
import requests
#from datetime import datetime

blueprint = Blueprint("jetradio", __name__, url_prefix="/jetradio")

@blueprint.route("/shoutout", methods=["POST"])
@auto_docs.doc()
def shoutout():
    """
        <h3>Send a Shoutout Request to Jet Radio</h3>
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
            curl -X GET "https://{{ request.host }}/jetradio/shoutout" -H "Content-Type: application/json" -d '{"name": "Josh", "message": "Hello! I'm on the M6 cruising, quite sweet."}'
        </code>
        <br>
        <p>Python Example:</p>
        <code>
            import requests<br>
            response = requests.post("https://{{ request.host }}/jetradio/shoutout", json={"name": "Josh", "message": "Hello! I'm on the M6 cruising, quite sweet."}<br>
            print(response.json())<br>
        </code>
    """
    if not request.json:
        return jsonify({"success": False, "error": "Missing JSON Data"})

    shoutout_name = request.json.get("name")
    shoutout_message = request.json.get("message")

    if not(shoutout_name and shoutout_message):
        return jsonify({"success": False, "error": "Missing Parameters"})

    discord_json = {
        "embeds": [
            {
            "title": ":exclamation: New Shoutout",
            "description": f"New Shoutout from `{request.remote_addr}`.",
            "color": 15818848,
            "fields": [
                {
                "name": "> **Name**",
                "value": f"{shoutout_name}"
                },
                {
                "name": "> **Message**",
                "value": f"{shoutout_message}"
                }
            ]
            }
        ],
        "username": "jetradio.live",
        "avatar_url": "https://file.coffee/u/cRaSt2kar.png"
    }
    resp = requests.post(getenv("SHOUTOUTS_URL"), json=discord_json)
    if resp.status_code in range(200, 299):
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})