FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    cron \
    fonts-liberation \
    libu2f-udev \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libgbm1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /etc/apt/trusted.gpg.d/google.gpg \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list \
    && apt-get update && apt-get install -y google-chrome-stable

RUN apt-get update && apt-get install -y build-essential libfreetype6-dev liblcms2-dev libjpeg-dev zlib1g-dev x11-apps

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir  -r requirements.txt
COPY fonts /app/fonts

RUN echo "* * * * * root cd /app && /usr/local/bin/python main.py >> /var/log/cron.log 2>&1" > /etc/cron.d/my-cron \
    && echo "" >> /etc/cron.d/my-cron \
    && chmod 0644 /etc/cron.d/my-cron \
    && crontab /etc/cron.d/my-cron \
    && touch /var/log/cron.log

ENV PYTHONUNBUFFERED=1

CMD ["cron", "-f"]