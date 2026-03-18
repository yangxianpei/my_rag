# 使用官方 Python
FROM python:3.13

# 设置工作目录
WORKDIR /app

# 复制项目文件（你的代码 + uv 配置 + requirements 或 pyproject.toml）
COPY . /app

# 安装 uv（你的本地 uv 工具）
RUN pip install uv

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
# 使用 uv sync 安装依赖

RUN uv sync --frozen --index-url https://pypi.tuna.tsinghua.edu.cn/simple
# 设置默认环境变量文件（可选）
ENV ENV_FILE=.env.prod

# 容器启动命令
CMD ["uv", "run", "main.py"]