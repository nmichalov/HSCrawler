#!/usr/bin/env python
"""
A well-behaved web crawler for gathering URLs.
"""

import urlparse
import mechanize
import re
import cPickle
from time import sleep

class Crawler:

    def __init__(self, crawler_id, crawl_limit):
        self.crawler_id = crawler_id
        self.crawl_limit = crawl_limit
        self.url_list = []
        self.visited = []
        self.failed_urls = []
        self.referrer_hash = {}
        self.br = mechanize.Browser()
        self.br.addheaders = [('user-agent', 'https://github.com/nmichalov')]
    
    def start(self, start_url):
        self.url_list.append(start_url)
        self.crawl()
    
    def crawl(self):
        while len(self.url_list) != 0 and len(self.visited) <= self.crawl_limit:
            target_url = self.url_list[0]
            print target_url
            url_parts = urlparse.urlparse(target_url)
            if url_parts.scheme == 'http':
                try:
                    response = self.br.open(target_url)
                    self.visited.append(target_url)
                    for link in list(self.br.links()):
                        if link.url.startswith('http:'):
                            link = link.url
                        else:
                            if not link.url.startswith('mailto:'):
                                link = link.base_url+link.url
                        if link not in self.url_list and link not in self.visited and link not in self.failed_urls:
                            self.url_list.append(link)
                        if urlparse.urlparse(link).hostname != url_parts.hostname:
                            if link not in self.referrer_hash:
                                self.referrer_hash[link] = [target_url,]
                            else:
                                if target_url not in self.referrer_hash[link]:
                                    self.referrer_hash[link].append(target_url)
                    sleep(1)
                except:
                    self.failed_urls.append(target_url)
            del self.url_list[0]
        self.report()
    
    def report(self):
        url_file = open(self.crawler_id+'-URLFile.txt', 'a')
        for url in self.visited:
            url_file.write(url+'\n')
        url_file.close()
        failed_file = open(self.crawler_id+'-FailedURLs.txt', 'a')
        for url in self.failed_urls:
            failed_file.write(url+'\n')
        failed_file.close()
        referrer_file = open(self.crawler_id+'-ReferrerHash.pck', 'w')
        cPickle.dump(self.referrer_hash, referrer_file)
        referrer_file.close()
                       

if __name__ == '__main__':
    #start_page = raw_input('Enter starting URL: ')
    #ident = raw_input('Designate an ID for this crawl: ')
    #limit = int(raw_input('Enter crawl limit: '))
    #NC = Crawler(ident, limit)
    #NC.start(start_page)
    NC = Crawler(str(0), 30)
    NC.start('http://www.hackerschool.com')
