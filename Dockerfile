# 1. 使用 slim 镜像
FROM python:3.13-slim

WORKDIR /app

# 2. 不从 GitHub 复制 uv，直接通过国内镜像安装 uv
RUN pip install uv -i https://mirrors.aliyun.com/pypi/simple/

# 3. 复制依赖文件
COPY pyproject.toml uv.lock* ./

# 4. 同步依赖（如果你不需要 GPU，这里一定要加 --extra-index-url）
# 这步如果也慢，是因为在下载 torch 等大包，阿里云镜像会快很多
RUN uv sync --frozen \
    --index-url https://mirrors.aliyun.com/pypi/simple/ \
    --extra-index-url https://download.pytorch.org/whl/cpu

# 5. 复制代码
COPY . .

CMD ["uv", "run", "main.py"]