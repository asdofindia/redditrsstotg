import config
import feedparser
import json
import requests
import os
import subprocess
import time

class RSStoTGbot(object):
    """docstring for RSStoTGbot"""
    def __init__(self):
        super(RSStoTGbot, self).__init__()
        self.subreddits = ""
        for sr in config.subreddits:
            self.subreddits += sr + "+"
        self.feedurl = "http://www.reddit.com/r/" + self.subreddits + "/.rss"
        self.refreshdownloads()
        if not os.path.exists("downloads"):
            os.makedirs("downloads")

    def refreshdownloads(self):
        if not os.path.isfile("downloaded"):
            with open("downloaded", 'w') as downloaded:
                downloaded.write("[]")
            self.downloads = []
        else:
            with open("downloaded","r") as downloaded:
                self.downloads = json.load(downloaded)

    def indownloads(self, link):
        if link in self.downloads:
            return True
        else:
            return False

    def addtodownloads(self, link):
        self.downloads.append(link)

    def writedownloads(self):
        with open("downloaded","w") as downloaded:
            json.dump(self.downloads, downloaded)

    def findlink(self, description):
        prelink = description.split('">[link]')[0]
        thelink = "http" + prelink.split("http")[-1]
        return thelink

    def directimage(self, link):
        for a in ["jpg", "jpeg", "gif", "png"]:
            if link.endswith(a):
                return True
        return False

    def download(self, link):
        filename = config.togroup + "-" + link.split('/')[-1]
        r = requests.get(link, headers=header)
        with open("downloads/"+filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
        return

    def sendtotg(self):
        subprocess.call(["./sender.sh", config.tgdir])

    def start(self):
        while True:
            print("polling feed")
            d = feedparser.parse(self.feedurl)
            self.topn = min(config.topn, len(d.entries))
            for entry in d.entries[:self.topn]:
                print("checking entry" + entry.title)
                link = self.findlink(entry.description)
                print("Found link:" + link)
                if self.directimage(link):
                    if (link is not None) and (not self.indownloads(link)):
                        print("New. Downloading")
                        self.download(link)
                        self.addtodownloads(link)
                else:
                    continue
            self.writedownloads()
            self.sendtotg()
            print("Going into deep sleep")
            time.sleep(config.waittime)


if __name__ == "__main__":
    bot = RSStoTGbot()
    bot.start()
