# SAP MCP Dockerfile
# 使用官方Python镜像作为基础
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 配置pip使用阿里云镜像源加速依赖安装（国内环境）
ENV PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
ENV PIP_TRUSTED_HOST=mirrors.aliyun.com

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 先复制requirements.txt，利用Docker缓存层
COPY requirements.txt .

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 创建日志目录
RUN mkdir -p /app/log

# 暴露端口
EXPOSE 8000
EXPOSE 8080

# 设置默认命令为启动Web管理界面
CMD ["python", "-m", "uvicorn", "web.main:app", "--host", "0.0.0.0", "--port", "8080"]
