__author__ = 'michaelstarin'

from RSS import RSSReader
import datetime
import os
import threading

input_file = open('/Users/michaelstarin/Desktop/Web_Recon/RssWebScraper/url_file_list', 'r')
url_list = input_file.readlines()
input_file.close()

now = datetime.datetime.now()

pickleDirRoot = '/Users/michaelstarin/Desktop/Web_Recon/Scraped_Data'
pickleDirDate = str(now.date())
pickleFileRoot = pickleDirRoot + '/' + pickleDirDate + '/'

try:
    os.makedirs(pickleFileRoot)
except OSError:
    pass


def call_method():
    instance = RSSReader(url_list[i], pickleFileRoot + fixed)
    instance.run_it()

for i in range(0, len(url_list)):
    a = str(url_list[i])
    b = a.replace("/","")
    fixed = b[5:]
    rss = threading.Thread(target=call_method)
    rss.start()