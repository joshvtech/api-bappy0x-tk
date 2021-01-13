from flask import Blueprint
from flask_selfdoc import Autodoc

blueprint = Blueprint("docs", __name__, url_prefix="/docs")

auto_docs = Autodoc()

@blueprint.route("/")
def index():
    return auto_docs.html(template="docs.html")