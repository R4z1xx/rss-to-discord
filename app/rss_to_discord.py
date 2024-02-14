import feedparser
import requests
import logging
import json
import time
import re
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)s|%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
log_formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(message)s')
logger = logging.getLogger()

rss_feed_urls = {
    'categ_name': ['https://rss.url/feed'],
    'second_categ': ['https://rss.url/feed']
}
webhook_url = {'categ_name': 'https://discord.com/api/webhooks/webhook.id/webhook.token'}

class FeedNotifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
        self.viewed_entries_file = 'viewed_entries.json'
        self.viewed_entries = self._load_viewed_entries()

    def _load_viewed_entries(self):
        if os.path.exists(self.viewed_entries_file):
            with open(self.viewed_entries_file, 'r') as f:
                return set(json.load(f))
        return set()

    def _save_viewed_entries(self):
        with open(self.viewed_entries_file, 'w') as f:
            json.dump(list(self.viewed_entries), f)

    def clean_html(self, text):
        clean = re.compile('<.*?>')
        cleaned_text = re.sub(clean, '', text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        return cleaned_text

    def send_articles(self, rss_feeds, type):
        for rss_feed in rss_feeds[type]:
            feed = feedparser.parse(rss_feed)
            for entry in feed.entries:
                if entry.id not in self.viewed_entries:
                    entry.summary = self.clean_html(entry.summary)
                    rss_feed_author = '.'.join(entry.title_detail['base'].split('/')[2].split('.')[-2:])
                    color = {
                        'domain.org':  0xffffff
                    }.get(rss_feed_author, None) # Modify this if you want to change the color of the embed on Discord (Default is None)
                    
                    embed = {
                        "title": entry.title,
                        "url": entry.link,
                        "description": entry.summary[:190] + ('...' if len(entry.summary) >  190 else ''),
                        "image": {"url": entry.media_content[0]['url'] if 'media_content' in entry else feed.feed.image['url']},
                        "color": color,
                        "fields": [{"name": "Published", "value": entry.published.split('+')[0]}],
                        "footer": {"text": f"From {rss_feed_author} RSS feed"}
                    }

                    headers = {'Content-Type': 'application/json'}
                    data = {
                        'username': rss_feed_author,
                        'avatar_url': feed.feed.image['url'],
                        'embeds': [embed]
                    }
                    response = requests.post(self.webhook_url[type], headers=headers, data=json.dumps(data))

                    if response.status_code ==  204:
                        logger.info(f"Message sent for entry: {entry.title}")
                        self.viewed_entries.add(entry.id)
                        self._save_viewed_entries()
                    else:
                        logger.error(f"An error occurred for entry: {entry.title}")

notifier = FeedNotifier(webhook_url)
while True:
    try:
        for rss_feed_type in rss_feed_urls:
            notifier.send_articles(rss_feed_urls, rss_feed_type)
    except Exception as e:
        logger.error(f'An error occurred: {e}')
        time.sleep(900) # Retries after 15 minutes
    logger.info('Waiting for 1 hour before checking for new articles...')
    time.sleep(3600) # Check for new articles every hour