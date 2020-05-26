from flask import Flask, jsonify, request
from flask_cors import CORS
from flaskext.markdown import Markdown

from os.path import join

from dotenv import load_dotenv
load_dotenv(override=True)
from os import getenv

from db.models import *

def create_app():
    app = Flask(__name__)

    app.jinja_env.globals.update(len=len)

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    CORS(app)
    Markdown(app)

    from views.docs import auto_docs, blueprint as docs_blueprint
    auto_docs.init_app(app)
    app.register_blueprint(docs_blueprint)

    @app.route("/")
    def index():
        return jsonify({"success": True})

    @app.route("/notifications", methods=["GET"])
    @auto_docs.doc()
    def list_notifications():
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
        notifs = notifications.query.all()
        requestParams = {}

        requestParams["valid"] = request.args.get("valid", default=True, type=bool)
        if requestParams["valid"]:
            notifs = [i for i in notifs if (i.timestamp == None) or (i.timestamp < datetime.now())]

        requestParams["removeImportant"] = request.args.get("removeImportant", default=False, type=bool)
        if requestParams["removeImportant"]:
            notifs = [i for i in notifs if not i.important]
        
        requestParams["maximum"] = request.args.get("max", default=5, type=int)
        notifs = notifs[:requestParams["maximum"]]

        notifs = [dict(i) for i in notifs]
        success = True

        return jsonify(**locals())

    return app

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=80, debug=True)