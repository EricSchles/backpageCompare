import requests
import time
import os
from glob import glob
import lxml.html

def webpage_grab(url):
    r = requests.get(url)
    name = "_".join(r.url.split("/")[-2:]).replace(".html")
    if not os.path.exists(name):
        os.mkdir(name)
    os.chdir(name)
    now = time.strftime("%m_%d_%y_%H")
    folder = os.path.join(os.getcwd(), name)
    html_files = [file for file in glob(os.path.join(folder,'*.html'))]
    html_files.sort(key=os.path.getmtime)
    most_recently_edited = html_files[-1]
    previous = open(most_recently_edited,"r")
    if r.text != previous:
        with open(name+now+".html","w") as f:
            f.write(r.text)
        
def map_website(base_url,depth=15):
    r = requests.get(base_url)
    links = []
    name = base_url.split("//")[1].split("/")[0]
    return mapper(base_url,urlname,links,depth)

def mapper(url,urlname,links,depth):
    if depth <= 0:
        return links
    r = requests.get(url)
    html = lxml.html.fromstr(r.text)
    tmp = html.xpath("//a/@href")
    for link in tmp:
        if urlname in link:
            tmp_links = mapper(link,urlname,links,depth-1)
            links += [link for link in tmp_links if not link in links]
            if not link in links:
                links.append(link)
    return links

