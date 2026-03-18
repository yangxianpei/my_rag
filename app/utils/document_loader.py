from app.utils.logger import get_logger
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from tempfile import NamedTemporaryFile
import os


logger = get_logger(__name__)


class DocumentLoader:
    @staticmethod
    def load_pdf(file_data):
        try:
            with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(file_data)
                tmp_path = tmp_file.name
            try:  # 其实在内部会根据页面进行分割，一个页面对应一个Document
                loader = PyPDFLoader(tmp_path)
                # documents会在加载的时候自动设置metadata
                documents = loader.load()
                return documents
            finally:
                # 最后手动删除临时文件
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

        except Exception as e:
            logger.error(f"加载PDF时出错:{e}")
            raise ValueError(f"加载PDF时出错:{e}")

    @staticmethod
    def load_docx(file_data):
        try:
            with NamedTemporaryFile(delete=False, suffix=".docx") as tmp_file:
                tmp_file.write(file_data)
                tmp_path = tmp_file.name
            try:
                loader = Docx2txtLoader(tmp_path)
                documents = loader.load()
                return documents
            finally:
                # 最后手动删除临时文件
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

        except Exception as e:
            logger.error(f"加载PDF时出错:{e}")
            raise ValueError(f"加载PDF时出错:{e}")

    @staticmethod
    def load_text(file_data):
        text = file_data.decode("utf-8")
        try:
            with NamedTemporaryFile(
                delete=False, suffix=".txt", mode="w", encoding="utf-8"
            ) as tmp_file:
                tmp_file.write(text)
                tmp_path = tmp_file.name
            try:
                loader = TextLoader(tmp_path, encoding="utf-8")
                documents = loader.load()
                return documents
            finally:
                # 最后手动删除临时文件
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

        except Exception as e:
            logger.error(f"加载PDF时出错:{e}")
            raise ValueError(f"加载PDF时出错:{e}")

    @staticmethod
    def load_md(file_data):
        try:
            with NamedTemporaryFile(delete=False, suffix=".md", mode="wb") as tmp_file:
                tmp_file.write(file_data)
                tmp_path = tmp_file.name
            try:
                loader = TextLoader(tmp_path)
                documents = loader.load()
                return documents
            finally:
                # 最后手动删除临时文件
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

        except Exception as e:
            logger.error(f"加载PDF时出错:{e}")
            raise ValueError(f"加载PDF时出错:{e}")

    @staticmethod
    def load(file_data, file_type):
        file_type = file_type.lower()
        if file_type == "pdf":
            return DocumentLoader.load_pdf(file_data)
        if file_type == "docx":
            return DocumentLoader.load_docx(file_data)
        if file_type in [
            "txt",
        ]:
            return DocumentLoader.load_text(file_data)
        if file_type == "md":
            return DocumentLoader.load_text(file_data)
        raise ValueError(f"不支持的文件类型:{file_type}")
