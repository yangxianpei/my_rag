FROM python:3.13-slim

WORKDIR /app

# --- 关键：先安装 uv 本身 ---
RUN pip install uv -i https://mirrors.aliyun.com/pypi/simple/

# 1. 先强行安装 CPU 版 torch 系列，占领坑位
# 注意：加上 --system 是因为在 Docker 容器内通常直接装在系统环境即可，无需再套一层虚拟环境
RUN uv pip install torch torchvision \
    --index-url https://download.pytorch.org/whl/cpu \
    --system

# 2. 复制配置文件
COPY pyproject.toml ./

# 3. 同步其他依赖
# 同样加上 --system，这样它会发现系统里已经有 torch 了
RUN uv sync --system --index-url https://mirrors.aliyun.com/pypi/simple/

COPY . .

CMD ["python", "main.py"]