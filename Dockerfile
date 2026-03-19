# 方案1：用更稳定的 Python 3.13-slim 官方镜像（优先推荐）
# 若仍拉取失败，换成方案2的 python:3.12-slim（兼容性更好）
FROM python:3.13-slim





WORKDIR /app

# 仅复制项目代码，不安装任何依赖
COPY . /app

# 安装 uv
RUN pip install --no-cache-dir uv

# 调用宿主机映射的 .venv 里的 uv 启动程序
CMD ["uv", "run", "main.py"]