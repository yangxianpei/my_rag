FROM python:3.13-slim

WORKDIR /app

# 基础优化
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 👉 先复制依赖文件（关键）
COPY pyproject.toml uv.lock* /app/

# 安装 uv
RUN pip install --no-cache-dir uv

# 👉 安装依赖（这一层会缓存）
RUN uv sync --frozen \
    --index-url https://mirrors.aliyun.com/pypi/simple/

# 👉 再复制代码（不会影响依赖缓存）
COPY . /app

# 环境变量
ENV ENV_FILE=.env.prod

CMD ["uv", "run", "main.py"]