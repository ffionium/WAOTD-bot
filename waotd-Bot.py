from distutils.command.clean import clean
from mimetypes import init
from bs4 import BeautifulSoup
from datetime import date
import re
import requests.auth
import praw

class waotdBot:

    # access main page, get href element
    def __gethrefLink__(self):
        content = requests.get('https://en.wikipedia.org/wiki/Main_Page')
        soup = BeautifulSoup(content.text, 'html.parser')
        divstring = soup.find('div', attrs={'id':"mp-tfa"})
        hreflinks = divstring.findAll('a', href=True)
        hrefLink = str(hreflinks[1])
        return hrefLink

    # parse out URL
    def __getURL__(self, hreflink):
        pattern = '"(.*?)"'
        strings = ' '.join((re.findall(pattern,hreflink)))
        pattern = '(\/wiki\S*)'
        urlString = ' '.join((re.findall(pattern,strings)))
        return urlString

    # parse out article title, create submission title
    def __getTitle__(self,hreflink):
        pattern = '"(.*?)"'
        strings = ' '.join((re.findall(pattern,hreflink)))        
        pattern = '(?<=\s).*'
        title = ' '.join((re.findall(pattern,strings)))
        today = date.today()
        d = str(today.strftime("%B %d, %Y"))
        title = title + ': ' + d
        return title

    # callout to reddit, submit post
    def __redditPost__(self, post, URLstring):

        postTitle = post

        reddit = praw.Reddit(
            client_id='fSMc7UDK19CWIA7MoHG02Q',
            client_secret='s1MZhpky-NULb-wlTdz6mbNEQQkGyA',
            password='vivivi22',
            user_agent='redditdev scraper by u/ffionium',
            username='WAOTD-bot'
            )

        subreddit = reddit.subreddit('ffioniumsbots')
        subreddit.submit(title=post, url=URLstring) 


waotdBot = waotdBot()

hreflink = waotdBot.__gethrefLink__()
URLstring = 'https://en.wikipedia.org/' + str(waotdBot.__getURL__(hreflink))
print(URLstring)

title = waotdBot.__getTitle__(hreflink)
post = title
print(post)

waotdBot.__redditPost__(post, URLstring)