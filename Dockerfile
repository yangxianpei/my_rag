FROM python:3.13-slim

WORKDIR /app

# 安装 uv
RUN pip install uv -i https://mirrors.aliyun.com/pypi/simple/

# 只要 pyproject.toml
COPY pyproject.toml ./

# 同步依赖：只需指定一个主镜像加速普通的包，torch 的逻辑交给 toml
RUN uv sync --index-url https://mirrors.aliyun.com/pypi/simple/

COPY . .
CMD ["python", "main.py"]