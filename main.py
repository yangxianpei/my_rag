from app import create_app
from app.config import Config
from app.utils.logger import get_logger
import os

logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info(f"正在启动项目")
    app = create_app()
    logger.info(f"正在启动RAG服务器在{Config.APP_HOST}:{Config.APP_PORT}")

    app.run(debug=True, host=Config.APP_HOST, port=Config.APP_PORT, threaded=True)
