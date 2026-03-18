# 使用 slim 版本可以进一步减小镜像基础体积
FROM python:3.13-slim

WORKDIR /app

# 1️⃣ 直接从官方 uv 镜像复制二进制文件，比 pip 安装更高效
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 2️⃣ 复制依赖文件
COPY pyproject.toml uv.lock* ./

# 3️⃣ 关键：安装依赖
# 如果你是为了避开 PyTorch 的 GPU 包，添加 --extra-index-url 
# 并利用 --no-cache 保持镜像轻量
RUN uv sync --frozen \
    --index-url https://mirrors.aliyun.com/pypi/simple/ \
    --extra-index-url https://download.pytorch.org/whl/cpu

# 4️⃣ 复制代码
COPY . .

# 5️⃣ 环境变量（可选）：强制程序在运行时也不去找显卡
ENV CUDA_VISIBLE_DEVICES=""

CMD ["uv", "run", "main.py"]