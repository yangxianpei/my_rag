from flask import Flask
import os
from app.config import Config
from flask_cors import CORS
from app.utils.auth import get_current_user
from app.utils.logger import get_logger

logger = get_logger(__name__)


# 导入初始化数据库函数
from app.utils.db import init_db


def create_app(config=Config):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    try:
        logger.info("初始化数据库...")
        init_db()
        logger.info("初始化数据库成功")
    except Exception as e:
        logger.warning(f"数据库初始化失败")
    app = Flask(
        import_name=__name__,
        static_folder=os.path.join(base_dir, "static"),
        template_folder=os.path.join(base_dir, "templates"),
    )

    @app.context_processor
    def inject_user():
        return dict(current_user=get_current_user())

    from app.blueprints import auth, knowledgebase, chat, settings, document

    app.register_blueprint(auth.bp)
    app.register_blueprint(knowledgebase.bp)
    app.register_blueprint(chat.bp)
    app.register_blueprint(settings.bp)
    app.register_blueprint(document.bp)
    app.secret_key = "aaabbccc"
    CORS(app)
    return app
