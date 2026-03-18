import hashlib
from app.models.user import User
from app.services.base_service import BaseService


class UserService(BaseService[User]):
    def hash_password(self, password):
        # 使用SHA256哈希算法进行哈希计算，
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def register(self, username, password, email):
        with self.transaction() as session:
            existing_user = session.query(User).filter_by(username=username).first()
            if existing_user:
                raise ValueError("用户名已经被占用")
            password_hash = self.hash_password(password)
            user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                is_active=True,
            )
            # 用户的ID是在插入数据库的时候生成的
            # 添加新的用户到会话中
            session.add(user)
            # 刷新用户实例，得到用户ID
            session.flush()
            self.logger.info(f"用户{username}注册成功")
            return user.to_dict()

    def verify_password(self, password, password_hash):
        return self.hash_password(password) == password_hash

    def login(self, username, password):
        if not username or not password:
            raise ValueError("用户名和密码不能为空")
        with self.session() as session:
            existing_user = session.query(User).filter_by(username=username).first()
            if not existing_user:
                raise ValueError("用户不存在")
            if not existing_user.is_active:
                raise ValueError("此用户已经被封禁")
            if not self.verify_password(password, existing_user.password_hash):
                raise ValueError("密码错误")
            self.logger.info(f"用户{username}登录成功")
            return existing_user.to_dict()

    def get_by_id(self, user_id):
        user = super().get_by_id(User, user_id)
        if user:
            return user.to_dict()
        else:
            return None


user_service = UserService()
