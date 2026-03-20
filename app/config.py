import os
from pathlib import Path
from dotenv import load_dotenv

env_name = os.getenv("ENV", "dev")  # 默认 dev
env_file = f".env.{env_name}"
load_dotenv(env_file)  # 加载环境变量
print(f"当前的环境变量是:{env_file}")


class Config:
    BASE_DIR = Path(__file__).parent.parent  # 根目录

    # 应用配置
    APP_HOST = os.environ.get("APP_HOST", "0.0.0.0")
    APP_PORT = os.environ.get("APP_PORT", 5000)
    APP_DEBUG = os.environ.get("APP_DEBUG", "false").lower() == "true"

    # 日志配置
    # 日志存放目录
    LOG_DIR = os.environ.get("LOG_DIR", "./logs")
    # 日志文件
    LOG_FILE = os.environ.get("LOG_FILE", "rag.log")
    # 日志级别
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    # 是否启用文件日志
    LOG_ENABLE_FILE = os.environ.get("LOG_ENABLE_FILE", "true").lower() == "true"
    # 是否启用控制台
    LOG_ENABLE_CONSOLE = os.environ.get("LOG_ENABLE_CONSOLE", "true").lower() == "true"

    # 数据库
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", 3306)
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "123456")
    DB_NAME = os.environ.get("DB_NAME", "rag")
    DB_CHARSET = os.environ.get("DB_CHARSET", "utf8mb4")

    # 图片
    MAX_FILE_SIZE = int(os.environ.get("MAX_FILE_SIZE", 104857600))  # 100M
    # 允许 上传的文件
    ALLOWED_EXTENSIONS = {"pdf", "docx", "txt", "md"}
    # 允许 上传的图片的扩展名
    ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    # 允许 上传的图片的最大大小，默认为5M
    MAX_IMAGE_SIZE = int(os.environ.get("MAX_IMAGE_SIZE", 5242880))

    # 存储的类型
    STORAGE_TYPE = os.environ.get("STORAGE_TYPE", "local")  # local / minio
    # 本地文件的存储目录
    STORAGE_DIR = os.environ.get("STORAGE_DIR", "./storages")

    # deepseek
    DEEPSEEK_CHAT_MODEL = os.environ.get("DEEPSEEK_CHAT_MODEL", "deepseek-chat")
    DEEPSEEK_API_KEY = os.environ.get(
        "DEEPSEEK_API_KEY", "sk-71998f076ef040ef91cd6b4dcd872b70"
    )
    DEEPSEEK_BASE_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

    # 指定 chroma向量数据库的本地存储目录
    CHROMA_PERSIST_DIRECTORY = os.environ.get("CHROMA_PERSIST_DIRECTORY", "./chroma_db")

    # 指定向量数据库的类型
    VECTOR_DB_TYPE = os.environ.get("VECTOR_DB_TYPE", "chroma")  # chroma 或 milvus
    # embedding_model_name
    EMBEDDING_MODEL_NAMME = os.environ.get(
        "EMBEDDING_MODEL_NAMME",
        "C:/Users/yxp/Desktop/rag_code-master/rag_code-master/5.rag-lite/all-MiniLM-L6-v2",
    )  # chroma 或 milvus
    # RERANK_MODEL_NAME
    RERANK_MODEL_NAME = os.environ.get(
        "RERANK_MODEL_NAME",
        "C:/Users/yxp/Desktop/rag_code-master/rag_code-master/5.rag-lite/ms-marco-MiniLM-L6-v2",
    )
