FROM python:3.11-slim

WORKDIR /opt/app-root/src

COPY requirements.txt /opt/app-root/src/

## Install system dependencies
USER root
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

## Upgrade pip and install requirements
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

USER 1001

COPY . /opt/app-root/src
ENV FLASK_APP=app
ENV PORT 3000

EXPOSE 3000

CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
