FROM python:3.13-slim

WORKDIR /app

# 1️⃣ 先复制依赖文件（利用缓存）
COPY pyproject.toml uv.lock* /app/

# 2️⃣ 安装 uv
RUN pip install --no-cache-dir uv

# 3️⃣ 安装依赖（会生成 .venv）
RUN uv sync --frozen \
    --index-url https://mirrors.aliyun.com/pypi/simple/

# 4️⃣ 再复制代码
COPY . /app

# 5️⃣ 使用 uv 运行（推荐用 uvicorn）
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]