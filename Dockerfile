FROM python:3.13-slim

WORKDIR /app

# 1. 直接安装 CPU 版文件（这就相当于把正确的东西强行塞进它的胃里）
RUN pip install \
    https://download.pytorch.org/whl/cpu/torch-2.5.1%2Bcpu-cp313-cp313-manylinux_2_28_x86_64.whl \
    --no-cache-dir

# 2. 复制你的配置文件
COPY pyproject.toml ./

# 3. 安装剩下的业务包（记得加 --no-deps 或者是先把 pyproject.toml 里的 torch 删掉）
# 否则它安装 sentence-transformers 时发现 torch 版本不对，可能又去重下
RUN pip install . -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir

COPY . .
CMD ["python", "main.py"]