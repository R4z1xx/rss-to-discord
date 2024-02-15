# <p align="center">RSS-TO-DISCORD</p>

## Prerequisites :
You need to have Docker installed.

## Setup
First clone the repo :
```
git clone https://github.com/R4z1xx/rss-to-discord.git
cd rss-to-discord
```
Open `rss_feeds.json` and `webhooks.json` located in `/app/urls/` with your favorite tool. <br>
Then modify both json files with the URLs of the RSS feeds you want and the URL of your discord webhook :  
```
rss_feeds.json

{
    "categ_name": ["https://rss.url/feed"],
    "second_categ": ["https://rss.url/feed"]
}
```
```
webhooks.json

{
    "categ_name": "https://discord.com/api/webhooks/{webhook.id}/{webhook.token}",
    "second_categ": "https://discord.com/api/webhooks/{webhook.id}/{webhook.token}"
}
```
***Info : if you modify these files while the container is already running, it will automatically retrieve the new feeds/webhooks at the next article check (24 hours by default).***

Build the Docker image :
```
docker build -t im-rss-to-discord .
```
And start the container (it runs indefinitely) : 
```
docker run -d -v ./app/urls/:/app/urls/ --name rss-to-discord im-rss-to-discord
```

## Optional
### Default check time
By default the script check for new articles every 24 hours but you can modify this by changing the seconds of the timeout env : 
```
docker run -d -e timeout=86400 -v ./app/urls/:/app/urls/ --name rss-to-discord im-rss-to-discord
```

### Change embed color
You can also add color to the Discord embed content for each RSS feed by modifying these lines with the hex code of the color you want. For example : 
```
color = {
    'sentinelone.com':  0x6b0aea
}.get(rss_feed_author, None) # Modify this if you want to change the color of the embed on Discord (Default is None)
```
![image](https://github.com/R4z1xx/rss-to-discord/assets/118757955/bf6cf8ae-f6a4-4daf-b104-bcbc8cb52f4d)

PS : You can use `docker logs rss-to-discord` to check for errors in the script logs.
