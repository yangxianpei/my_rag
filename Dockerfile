# 使用轻量 Python 镜像（建议指定版本，和宿主机一致，比如 3.13-slim）
FROM python:3.13

WORKDIR /app

# 仅复制项目代码（不安装任何依赖、不装 uv）
COPY . /app

# 【核心】直接调用宿主机映射过来的 .venv 里的 uv 启动
# 路径必须和 docker-compose.yml 中映射的 .venv 一致：/app/.venv
CMD ["/app/.venv/bin/uv", "run", "main.py"]