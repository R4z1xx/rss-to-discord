# docker build -t im-rss-to-discord .
# docker run -d -e timeout=86400 -v ./app/urls/:/app/urls/ --name rss-to-discord im-rss-to-discord

FROM python:3.12-slim

WORKDIR /app
COPY ./app/ /app/
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "rss_to_discord.py"]