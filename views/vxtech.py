from flask import Blueprint, request, jsonify, abort
from .docs import auto_docs

from sys import path
path.append("...")
from db.models import tblVxTech_bank

blueprint = Blueprint("vxtech", __name__, url_prefix="/vxtech")

@blueprint.route("/request")
@auto_docs.doc()
def listener_request():
    """
        <h3>Send a Listener Request to Jet Radio</h3>
    """
    return jsonify({"success": False})