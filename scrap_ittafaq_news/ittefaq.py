import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
import webbrowser as wb

url = "https://www.ittefaq.com.bd/"
response = requests.get(url)
content = response.content
soup = BeautifulSoup(content,'html.parser')
#print(soup)

news = soup.find_all(['h1','h2','h3','h4'])
htmltext = '''
<html>
    <head>
        <title> Ittefaq News list </title>
    </head>
    <body>
        {NEWS_LINKS}
    </body>
</html>

'''
news_links = '<ol>'
for tag in news:
    if tag.parent.get('href'):
        link = tag.parent.get('href')
        title = tag.string
        news_links +="<li><a href = '{}' target='_blank'>{}</li>\n".format(link,title)

news_links += '</ol>'
htmltext = htmltext.format(NEWS_LINKS=news_links)
print(htmltext)


filename = "newslink.html"
with open(filename,"w",encoding=response.encoding) as fb:
    fb.write(htmltext)

filepath = os.path.realpath("newslink.html")
print(filename)
wb.open(filepath)
