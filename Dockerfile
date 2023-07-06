# Use alpine as base image
FROM python:3.8-alpine

# Install necessary packages
RUN apk update && \
    apk add --no-cache \
    git \
    redis \
    gcc \
    libc-dev \
    libffi-dev \
    openssl-dev \
    jpeg-dev \
    zlib-dev

# Start Redis server in the background
CMD ["sh", "-c", "redis-server --daemonize yes && /var/www/namizun/venv/bin/python3 /var/www/namizun/uploader.py & tail -f /dev/null"]

# Create project directory and clone the repository
RUN mkdir -p /var/www/namizun && \
    cd /var/www/namizun && \
    git init && \
    git remote add origin https://github.com/malkemit/namizun.git && \
    git pull origin master

# Create virtual environment
RUN python3 -m venv /var/www/namizun/venv

# Set the virtual environment as the active Python environment
ENV PATH="/var/www/namizun/venv/bin:$PATH"

# Upgrade pip and install wheel
RUN /var/www/namizun/venv/bin/python -m pip install --upgrade pip && \
    /var/www/namizun/venv/bin/pip install wheel

# Install project requirements
COPY namizun_core/ /var/www/namizun/namizun_core/
COPY namizun_menu/ /var/www/namizun/namizun_menu/
RUN /var/www/namizun/venv/bin/pip install /var/www/namizun/namizun_core/ /var/www/namizun/namizun_menu/

# Create namizun command
COPY else/namizun /usr/local/bin/namizun
RUN chmod +x /usr/local/bin/namizun

# Set the working directory
WORKDIR /var/www/namizun
