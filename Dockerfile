# docker build -t rss-to-discord .
# docker run -d --name rss-to-discord rss-to-discord

FROM python:3.12-slim

WORKDIR /app
COPY ./app/ /app/
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "rss_to_discord.py"]