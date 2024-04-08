import os
import requests
import grasslibs.getMcDir as mcd
import json

def getGithubRepo():
    return "https://github.com/JulenRa-dev/GrassLaunch-requests/raw/main/"

def getNewsJson():
    newsJsonLink = os.path.join(getGithubRepo(), "news", "news_links.json")
    try:
        newsJson = requests.get(newsJsonLink, timeout=3)
    except TimeoutError:
        return "Can'tConnect"
    newsJson = newsJson.text
    newsDict = json.loads(newsJson)
    return newsDict

def getLatestNews():
    newsDict = getNewsJson()
    latestNewsLink = os.path.join(getGithubRepo(), "news", newsDict["latest"])
    latestNews = requests.get(latestNewsLink)
    return latestNews.text