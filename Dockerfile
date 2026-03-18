FROM python:3.13

WORKDIR /

# 安装 uv
RUN pip install uv

# 安装依赖（关键）
RUN uv sync --frozen
