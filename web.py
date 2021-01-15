from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
from db.models import *

from os import getenv

def create_app():
    app = Flask(__name__)

    app.jinja_env.globals.update({
        "len": len,
        "render_template_string": render_template_string
    })

    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{getenv('DATABASE_URI')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    CORS(app)

    from views.notifications import blueprint as notifications_blueprint
    app.register_blueprint(notifications_blueprint)

    from views.jetradio import blueprint as jetradio_blueprint
    app.register_blueprint(jetradio_blueprint)

    from views.vxtech import blueprint as vxtech_blueprint
    app.register_blueprint(vxtech_blueprint)

    from views.docs import auto_docs, blueprint as docs_blueprint
    auto_docs.init_app(app)
    app.register_blueprint(docs_blueprint)

    #Error Handlers
    @app.errorhandler(403)
    def not_found(description):
        error = 403
        description = str(description)
        return jsonify(**locals()), error

    @app.errorhandler(404)
    def not_found(description):
        error = 404
        description = str(description)
        return jsonify(**locals()), error
        
    @app.errorhandler(500)
    def not_found(description):
        error = 500
        description = str(description)
        return jsonify(**locals()), error

    @app.route("/")
    def index():
        return jsonify({"success": True})

    return app

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=80, debug=True)