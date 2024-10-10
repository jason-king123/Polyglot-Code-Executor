# 使用带有Python环境的基础镜像
FROM registry.cn-wulanchabu.aliyuncs.com/zhanglonghui/python:3.8-slim

# 更新软件包列表并安装通用工具和编译器
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    vim \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# 安装C++环境
RUN apt-get update && apt-get install -y g++

# 安装C#环境 Mono
RUN apt-get update && apt-get install -y mono-devel

# 安装 Go
RUN apt-get update && apt-get install -y golang-go
ENV GOPATH=/go
RUN mkdir -p $GOPATH/bin
ENV PATH=$PATH:$GOPATH/bin

# 安装Java环境
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk && \
    rm -rf /var/lib/apt/lists/* && \
    java --version

# 安装Node.js环境

ENV NODE_VERSION=14
# RUN curl -fsSLO --compressed "https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-x64.tar.xz" \
#     && tar -xJf "node-v$NODE_VERSION-linux-x64.tar.xz" -C /usr/local --strip-components=1 --no-same-owner \
#     && rm "node-v$NODE_VERSION-linux-x64.tar.xz"

# 复制 Node.js 压缩包到镜像中
COPY ./dependencies/node-v14.17.0-linux-x64.tar.xz /usr/local/

# 解压 Node.js 压缩包
RUN tar -xJf /usr/local/node-v14.17.0-linux-x64.tar.xz -C /usr/local --strip-components=1 --no-same-owner \
    && rm /usr/local/node-v14.17.0-linux-x64.tar.xz

# 设置 Node.js 环境变量
ENV PATH=/usr/local/bin:$PATH

# 安装Kotlin环境
ENV KOTLIN_VERSION=1.4.21
RUN curl -sSLO "https://github.com/JetBrains/kotlin/releases/download/v$KOTLIN_VERSION/kotlin-compiler-$KOTLIN_VERSION.zip" \
    && unzip kotlin-compiler-$KOTLIN_VERSION.zip -d /usr/local/share \
    && rm kotlin-compiler-$KOTLIN_VERSION.zip \
    && ln -s /usr/local/share/kotlinc/bin/kotlinc /usr/local/bin/kotlinc

# 安装PHP环境
RUN apt-get update && apt-get install -y php-cli

# 安装Ruby环境
RUN apt-get update && apt-get install -y ruby-full

# 安装Rust环境
ENV RUSTUP_HOME=/usr/local/rustup
ENV CARGO_HOME=/usr/local/cargo
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y \
    && chmod -R a+w $RUSTUP_HOME $CARGO_HOME

# 安装Swift环境
# RUN apt-get update && apt-get install -y libswift-dev swiftlang
# 下载 Swift 压缩包
COPY ./dependencies/swift-6.0-RELEASE-ubuntu20.04.tar.gz /usr/local/
# 解压 Swift 压缩包
RUN tar -xzf /usr/local/swift-6.0-RELEASE-ubuntu20.04.tar.gz -C /usr/local --strip-components=1 \
    && rm /usr/local/swift-6.0-RELEASE-ubuntu20.04.tar.gz
# 设置 Swift 环境变量
ENV PATH="/usr/local/bin:${PATH}"

# 安装R环境
RUN apt-get update && apt-get install -y r-base

# 安装.NET Core环境
RUN apt-get update && apt-get install -y apt-transport-https && \
    curl https://packages.microsoft.com/config/debian/10/packages-microsoft-prod.deb -sSL | apt-get install -y

# 设置工作目录
WORKDIR /app

# 复制Python依赖文件
COPY requirements.txt /app/

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制多语言源代码
COPY . /app

# 暴露端口
EXPOSE 9999

# 设置默认启动命令
CMD ["python", "app.py"]