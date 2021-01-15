from flask import Blueprint, request, jsonify, abort
from .docs import auto_docs

from sys import path
path.append("...")
from db.models import db, tblVxTech_tokens, tblVxTech_bank

blueprint = Blueprint("vxtech", __name__, url_prefix="/vxtech")

@blueprint.route("/bank/<int:placeId>/<int:userId>")
@auto_docs.doc()
def bank(placeId, userId):
    """
        <h3>Get a user's saved informattion from the VxTech Bank</h3>
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
                    <td>token</td>
                    <td>string</td>
                    <td>None</td>
                    <td>This is the access token used to access data.</td>
                </tr>
            </tbody>
        </table>
        <br>
        <h4>Examples:</h4>
        <p>Raw URL:</p>
        <a href="{{ url_for('vxtech.bank', placeId=432, userId=123) }}?token=e36b9fd7cd944b71b9e71a2868b70650" target="_blank">https://{{ request.host }}{{ url_for('vxtech.bank', placeId=432, userId=123) }}?token=e36b9fd7cd944b71b9e71a2868b70650 <i class="fas fa-external-link-alt align-text-top" style="font-size: 0.5rem"></i></a>
        <p>cURL Example:</p>
        <code>
            curl -X GET "https://{{ request.host }}{{ url_for('vxtech.bank', placeId=432, userId=123) }}" -d token=e36b9fd7cd944b71b9e71a2868b70650
        </code>
        <br>
        <p>Python Example:</p>
        <code>
            import requests<br>
            response = requests.get("https://{{ request.host }}{{ url_for('vxtech.bank', placeId=432, userId=123) }}", params={"token": "e36b9fd7cd944b71b9e71a2868b70650"})<br>
            print(response.json())<br>
        </code>
    """
    print(placeId, userId)
    tokens = tblVxTech_tokens.query.filter_by(placeId=placeId).all()
    print(tokens)
    if not tokens or not any([i.checkToken(request.args.get("token")) for i in tokens]): return abort(403)

    result = tblVxTech_bank.query.filter_by(placeId=placeId, userId=userId).first_or_404()
    return jsonify({"success": True, "result": dict(result)})

@blueprint.route("/token/create")
@auto_docs.doc()
def createToken():
    """
        <h3>Create a token for VxTech</h3>
        <p>The token will only display on the back end, avoid using this - purely temporary</p>
    """
    newToken = tblVxTech_tokens()
    newToken.generateToken()
    db.session.add(newToken)
    db.session.commit()
    return jsonify({"success": True, "result": newToken.token})