# 基础Dockerfile，适用于国内环境
FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/library/python:3.10

# 设置pip国内镜像源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/ && \
    pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 安装项目
RUN pip install --no-cache-dir -e .

# 创建日志目录
RUN mkdir -p /app/log

# 暴露端口
EXPOSE 8000 8080

# 设置默认入口点为Web服务
CMD ["python", "-m", "uvicorn", "web.main:app", "--host", "0.0.0.0", "--port", "8080"]