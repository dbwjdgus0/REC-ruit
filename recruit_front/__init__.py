from flask import Flask, url_for


def create_app():

    app = Flask(__name__)

    # 블루프린트
    from .views import main_views
    app.register_blueprint(main_views.bp)


    return app

