FROM python:3.13-slim

WORKDIR /app

# 换成清华大学的 PyTorch CPU 镜像源
RUN pip install torch torchvision torchaudio \
    --index-url https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/linux-64/ \
    --extra-index-url https://mirrors.aliyun.com/pypi/simple/ \
    --no-cache-dir

# 2. 复制你的配置文件
COPY pyproject.toml ./

# 3. 关键：用 pip 安装剩下的依赖
# --no-deps 是终极手段：如果安装某个库（如 sentence-transformers）
# 报错说缺依赖，我们就手动补。如果它想自动装 torch-cuda，
# 因为我们第一步已经装了 torch，pip 通常会直接跳过。
RUN pip install . -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir

# 4. 复制代码
COPY . .

CMD ["python", "main.py"]