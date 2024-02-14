# RSS-TO-DISCORD - Documentation

## Prerequisites :
You need to have Docker installed.

## Setup
First clone the repo :
```
git clone https://github.com/R4z1xx/rss-to-discord.git
cd rss-to-discord
```
Open ```rss_to_discord.py``` located in ```rss-to-discord/app/``` with your favorite tool. <br>
Then modify these lines with the URLs of the RSS feeds you want and the URL of your discord webhook :  
```
rss_feed_urls = {
    'categ_name': ['https://rss.url/feed'],
    'second_categ': ['https://rss.url/feed']
}
webhook_url = {'categ_name': 'https://discord.com/api/webhooks/webhook.id/webhook.token'}
```

Build the Docker image :
```
docker build -t im-rss-to-discord .
```
And start a new container (it turns indefinitely) : 
```
docker run -d --name rss-to-discord im-rss-to-discord
```

## Optional
### Default check time
By default the script check for new articles every hour but you can modify this by changing the seconds on this line : 
```
time.sleep(3600) # Check for new articles every hour
```

### Change embed color
You can also add color to the Discord embed content for each RSS feed by modifying these lines with the hex code of the color you want : 
```
color = {
    'domain.org':  0xffffff
.get(rss_feed_author, None) # Modify this if you want to change the color of the embed on Discord (Default is None)
```
For example : <br>
![image](https://github.com/R4z1xx/rss-to-discord/assets/118757955/bf6cf8ae-f6a4-4daf-b104-bcbc8cb52f4d)
