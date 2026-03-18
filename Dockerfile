FROM python:3.13-slim

WORKDIR /app



# 2. 复制依赖文件
COPY pyproject.toml uv.lock* ./

# 1. 先强行安装 CPU 版 torch 系列，占领 .venv 坑位
RUN uv pip install torch torchvision \
    --index-url https://download.pytorch.org/whl/cpu

# 2. 再进行同步。uv 发现环境里已经有满足要求的 torch 了，
# 就不会再去 PyPI 触发那一堆 nvidia 级联下载
RUN uv sync --index-url https://mirrors.aliyun.com/pypi/simple/

# 4. 复制剩余代码
COPY . .

CMD ["uv", "run", "main.py"]