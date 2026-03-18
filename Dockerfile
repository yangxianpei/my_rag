# 方案1：用更稳定的 Python 3.13-slim 官方镜像（优先推荐）
# 若仍拉取失败，换成方案2的 python:3.12-slim（兼容性更好）
FROM python:3.13-slim

# 可选：手动配置国内镜像源（解决依赖拉取问题，即使我们不用，也避免基础镜像问题）
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    apt update && apt install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 仅复制项目代码，不安装任何依赖
COPY . /app

# 调用宿主机映射的 .venv 里的 uv 启动程序
CMD ["/app/.venv/bin/uv", "run", "main.py"]