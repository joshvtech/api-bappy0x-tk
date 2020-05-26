from flask import Flask, jsonify
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
    def notifications_get():
        """
Get notifications
=================

> this is a codeblock

this is an _em_.

Form data: test

```
this is code
```
        """
        valid = []
        currentTime = datetime.now()
        for i in notifications.query.filter_by(timestamp=None).all() + notifications.query.filter(notifications.timestamp!=None).order_by(notifications.timestamp).all():
            #.limit(4)
            """if i.timestamp and i.timestamp > currentTime: #TODO: Add this to the query instead
                continue"""
            valid.append(dict(i))
        return jsonify(success=True, valid=valid)

    return app

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=80, debug=True)