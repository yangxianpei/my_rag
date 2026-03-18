# 使用官方 Python
FROM python:3.13

# 设置工作目录
WORKDIR /app

# 复制项目文件（你的代码 + uv 配置 + requirements 或 pyproject.toml）
COPY . /app

# 安装 uv（你的本地 uv 工具）
RUN pip install uv

# 使用 uv sync 安装依赖

RUN uv sync --index-url https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
# 设置默认环境变量文件（可选）
ENV ENV_FILE=.env.prod

# 容器启动命令
CMD ["uv", "run", "main.py"]