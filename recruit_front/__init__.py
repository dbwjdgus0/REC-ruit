from flask import Flask, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


import config

db = SQLAlchemy()
migrate = Migrate()                 # 전역 변수로 db, migrate 객체를 만들어 create_app 함수 안에 init_app 메서드를 이용해 초기화
                                    # db객체를 create_app 함수 안에서 생성하면 블루프린트와 같은 다른 모듈을 불러올 수 없음


def create_app():

    app = Flask(__name__)
    app.config.from_object(config)  # config.py 파일에 작성한 항목을 app.config 환경변수로 부르기 위해 작성

    # 블루프린트
    from .views import main_views
    app.register_blueprint(main_views.bp)


    # ORM
    db.init_app(app)
    migrate.init_app(app, db)

    return app

