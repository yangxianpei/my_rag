from abc import ABC, abstractmethod


class VectorDBInterface(ABC):
    @abstractmethod
    def get_or_create_collection(self, collection_name):
        """
         获取或创建集合

        :param collection_name: 集合名称
        """
        pass

    @abstractmethod
    def add_documents(self, collection_name, documents, ids):
        """
         添加文档到向量存储

        :param collection_name: 集合名称
        """
        pass

    @abstractmethod
    def delete_documents(self, collection_name, ids=None, filter=None):
        """
         获取或创建集合

        :param collection_name: 集合名称
        """
        pass

    @abstractmethod
    def similarity_search_with_score(self, collection_name, query, k, filter):
        pass
