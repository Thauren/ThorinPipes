#!/usr/bin/python
#coding=utf-8

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import feedparser
import datetime
import PyRSS2Gen
import time

def cinema_filter(arg):
    return ((arg.find('2015') != -1 or arg.find('2014') != -1) 
        and ((arg.find('HD') != -1) or (arg.find('1080') != -1) or (arg.find('720') != -1)))                

def humor_filter(arg):
    return (((arg.find('HD') != -1) or (arg.find('1080') != -1) or (arg.find('720') != -1))
        and ((arg.find(u'КВН') != -1) or (arg.find(u'Уральские пельмени') != -1)))                

config = [
            ('http://alt.rutor.org/rss.php?category=1', cinema_filter, 'зарубежные'),
            ('http://alt.rutor.org/rss.php?category=5', cinema_filter, 'наши'),
            ('http://alt.rutor.org/rss.php?category=7', cinema_filter, 'мультики'),
            ('http://alt.rutor.org/rss.php?category=15', humor_filter, 'юмор')
        ]

class HttpProcessor(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type','text/rss+xml')
        self.end_headers()

        if self.path == '/rss':
            items = []
            for url, filt, name in config:
                d = feedparser.parse(url)
                group = [PyRSS2Gen.RSSItem(
                    title = x.title,
                    link = x.link,
                    description = x.summary,
                    guid = x.link,
                    pubDate = datetime.datetime.utcfromtimestamp(time.mktime(x.published_parsed)))
                    for x in d.entries if filt(x.title)]
                print name + ' generate ' + str(len(group)) + ' elements'
                items = items + group

            # # make the RSS2 object
            rss = PyRSS2Gen.RSS2(
                title = d.feed.title,
                link = d.feed.link,
                description = "thorin's Filtered RSS Feed",
                lastBuildDate = datetime.datetime.now(),
                items = items)
            rss.write_xml(self.wfile)
            print 'All generated ' + str(len(items)) + ' elements'

print "Script started"
serv = HTTPServer(("localhost",8800), HttpProcessor)
serv.serve_forever()
