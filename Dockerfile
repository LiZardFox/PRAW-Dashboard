FROM python:3.9-slim

RUN apt-get update && apt-get install -y cron

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash", "-c", "echo '0 0 * * * python /app/daily_script.py' > /etc/cron.d/daily_task && \
                      echo '0 * * * * python /app/hourly_script.py' > /etc/cron.d/hourly_task && \
                      chmod 0644 /etc/cron.d/daily_task /etc/cron.d/hourly_task && \
                      crontab /etc/cron.d/daily_task /etc/cron.d/hourly_task && \
                      touch /var/log/cron.log && \
                      cron && tail -f /var/log/cron.log"]
