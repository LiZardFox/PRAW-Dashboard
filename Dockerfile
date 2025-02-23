FROM python:3.9-slim

RUN apt-get update && apt-get install -y cron

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY cron_jobs /etc/cron_jobs
RUN touch /var/log/cron.log && crontab /etc/cron_jobs

CMD ["cron", "-f"]
