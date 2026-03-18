from app.config import Config
from app.services.storage.local_storage import LocalStorage


class StorageFactory:
    _instance = None

    @classmethod
    def create_storage(cls, **kwargs):
        storage_type = getattr(Config, "STORAGE_TYPE", "local").lower()
        if storage_type == "local":
            return LocalStorage()
        else:
            raise ValueError(f"不支持的存储类型:{storage_type}")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls.create_storage()
        return cls._instance


storage_service = StorageFactory.get_instance()
