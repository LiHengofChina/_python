# 使用官方的Python 3镜像作为基础镜像
FROM python:3.8-slim

# 设置工作目录
WORKDIR /app

# 将当前目录中的文件复制到镜像中的工作目录
COPY . /app

# 运行Python程序
CMD ["python", "app.py"]
