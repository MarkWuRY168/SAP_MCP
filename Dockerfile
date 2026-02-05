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

# 安装Python和系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip \
    python3.10-dev \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/* \
    && ln -s /usr/bin/python3.10 /usr/bin/python

# 复制requirements.txt先安装依赖（利用Docker层缓存）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 安装项目
RUN pip install --no-cache-dir -e .

# 创建日志目录
RUN mkdir -p /app/log

# 暴露端口
# MCP服务器端口
EXPOSE 8000
# Web管理界面端口
EXPOSE 8080

# 设置默认入口点（可通过docker-compose覆盖）
CMD ["sap-mcp-server"]