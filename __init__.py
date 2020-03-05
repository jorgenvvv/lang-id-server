from flask import Flask, jsonify, g, render_template, send_from_directory
from flask_cors import CORS

from .constants import *
from .language_identifier import LanguageIdentifier


def create_app():
    from .config import Config
    from .api import api

    app = Flask(
        __name__,
        instance_relative_config=True,
        static_folder='./public/static',
        template_folder='./public'
    )

    CORS(app)

    app.config.from_object(Config)

    app.register_blueprint(api)

    with app.app_context():
        app.language_identifier = LanguageIdentifier()

    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({'error': constants.FILE_TOO_LARGE_ERROR}), 413

    @app.route('/', defaults={'path': '/'})
    @app.route('/<path:path>')
    def index(path):
        return render_template('index.html')

    @app.route('/assets/<path:path>')
    def get_assets(path):
        return send_from_directory('./public/assets', path)


    return app
