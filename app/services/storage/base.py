from abc import ABC, abstractmethod


class StorageInterface(ABC):

    def upload_file(self, file_path, file_data):
        pass

    @abstractmethod
    def download_file(self, file_path):
        """
        下载文件

        :param file_path: 文件路径 相对路径

        return: 文件数据bytes
        """
        pass

    @abstractmethod
    def delete_file(self, file_path):
        """
        删除文件

        :param file_path: 文件路径 相对路径
        """
        pass

    @abstractmethod
    def file_exists(self, file_path):
        """
        判断文件是否存在

        :param file_path: 文件路径 相对路径
        """
        pass

    @abstractmethod
    def get_file_url(self, file_path):
        """
        获取文件访问URL地址

        :param file_path: 文件路径 相对路径
        Return 文件URL
        """
        pass
