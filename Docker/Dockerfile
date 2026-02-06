# 使用官方Ubuntu Python基础镜像
FROM ubuntu:22.04

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
# 配置pip使用阿里云镜像源加速依赖安装
ENV PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
ENV PIP_TRUSTED_HOST=mirrors.aliyun.com

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# 创建软链接，确保pip命令可用
RUN ln -sf /usr/bin/python3 /usr/bin/python && ln -sf /usr/bin/pip3 /usr/bin/pip

# 复制项目文件
COPY . /app

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 安装项目
RUN pip install --no-cache-dir .

# 创建日志目录
RUN mkdir -p /app/log

# 暴露端口
# MCP服务器端口
EXPOSE 8000
# Web管理界面端口
EXPOSE 8080

# 设置默认入口点为Web服务
CMD ["python", "-m", "uvicorn", "web.main:app", "--host", "0.0.0.0", "--port", "8080"]