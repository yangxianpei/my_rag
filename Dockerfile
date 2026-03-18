FROM python:3.13-slim

WORKDIR /app

# 1️⃣ 先复制依赖文件（利用缓存）
COPY pyproject.toml uv.lock* /app/

# 2️⃣ 安装 uv
RUN pip install --no-cache-dir uv

RUN uv sync --frozen --index-url https://mirrors.aliyun.com/pypi/simple/

# 4️⃣ 再复制代码
COPY . /app


CMD ["uv", "run", "main.py"]