# 使用官方Python基础镜像
FROM python:3.10-slim

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY . /app

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 安装项目
RUN pip install --no-cache-dir -e .

# 创建日志目录
RUN mkdir -p /app/log

# 暴露端口
EXPOSE 8000  # MCP服务器端口
EXPOSE 8080  # Web管理界面端口

# 设置默认入口点（可通过docker-compose覆盖）
CMD ["sap-mcp-server"]