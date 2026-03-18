FROM python:3.13-slim

WORKDIR /app

# 1. 安装 uv
RUN pip install uv -i https://mirrors.aliyun.com/pypi/simple/

# 2. 复制依赖文件
COPY pyproject.toml uv.lock* ./

# 3. 极简同步：不再需要命令行传多个 index，uv 会自动看 pyproject.toml
# 我们手动指定一个主镜像源即可
RUN uv sync --index-url https://mirrors.aliyun.com/pypi/simple/

# 4. 复制剩余代码
COPY . .

CMD ["uv", "run", "main.py"]