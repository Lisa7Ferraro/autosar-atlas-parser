FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    liblcms2-dev \
    libopenjp2-7 \
    libtiff-dev \
    libxml2-dev \
    libxslt1-dev \
    libffi-dev \
    libpq-dev \
    build-essential \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*


# 作業ディレクトリ
WORKDIR /workspace

# ここで全てのファイルをコピー
COPY . .

# Python環境設定
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# vscode ユーザー作成（devcontainer用）
RUN useradd -m vscode
USER vscode

# Pythonパッケージのインストール
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
