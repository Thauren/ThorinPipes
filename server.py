#!/usr/bin/python
#coding=utf-8

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import feedparser
import datetime
import PyRSS2Gen
import time
import re
import config

def filter_re(arg, text):
    result = True
    for f in arg:
        if f.search(text) == None:
            result = False
    return result

class HttpProcessor(BaseHTTPRequestHandler):

    def do_GET(self):
        start_time = time.time()
        self.send_response(200)
        self.send_header('content-type','text/rss+xml')
        self.end_headers()

        if self.path == '/rss':
            items = []
            for url, filt, name in config.config:
                d = feedparser.parse(url)
                group = [PyRSS2Gen.RSSItem(
                    title = x.title,
                    link = x.link,
                    description = x.summary,
                    guid = x.link,
                    pubDate = datetime.datetime.utcfromtimestamp(time.mktime(x.published_parsed)))
                    for x in d.entries if filter_re(filt, x.title)]
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
            print("--- %s seconds ---" % (time.time() - start_time))


print "Script started"
serv = HTTPServer(("localhost",8801), HttpProcessor)
serv.serve_forever()
