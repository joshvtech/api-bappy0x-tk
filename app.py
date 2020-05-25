from flask import Flask, jsonify
from flask_cors import CORS

from os.path import join

from dotenv import load_dotenv
load_dotenv(override=True)
from os import getenv

from db.models import *

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    CORS(app)

    @app.route("/")
    def index():
        return jsonify({"success": True})

    @app.route("/notifications", methods=["GET"])
    def notifications_get():
        valid = []
        currentTime = datetime.now()
        for i in notifications.query.filter_by(timestamp=None).all() + notifications.query.filter(notifications.timestamp!=None).order_by(notifications.timestamp).limit(4).all():
            if i.timestamp and i.timestamp > currentTime:
                continue
            valid.append(dict(i))
        return jsonify(success=True, valid=valid)

    return app

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=80, debug=True)