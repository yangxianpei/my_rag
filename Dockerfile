FROM python:3.13-slim

WORKDIR /app

# 1️⃣ 安装 uv（继续用国内镜像，快）
RUN pip install uv -i https://mirrors.aliyun.com/pypi/simple/

# 2️⃣ 复制依赖文件
COPY pyproject.toml uv.lock* ./

# 3️⃣ 关键：添加 --index-strategy 参数解决版本冲突
# 这会强制 uv 在所有源里寻找最合适的 requests 等基础库版本
RUN uv sync \
    --index-url https://mirrors.aliyun.com/pypi/simple/ \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    --index-strategy unsafe-best-match

# 4️⃣ 复制代码
COPY . .

# 告诉项目在运行时也别去找显卡
ENV CUDA_VISIBLE_DEVICES=""

CMD ["uv", "run", "main.py"]