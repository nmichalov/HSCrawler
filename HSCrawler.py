#!/usr/bin/env python
"""
A well-behaved web crawler for gathering URLs.
"""

import urlparse
import urllib2
import mechanize
import re
import cPickle
import os
import sys
from time import sleep

class Crawler:

    def __init__(self, crawler_id, crawl_limit):
        self.crawler_id = crawler_id
        self.crawl_limit = crawl_limit
        self.url_list = []
        self.visited = []
        self.atypical_urls = []
        self.referrer_hash = {}
        self.br = mechanize.Browser()
        self.br.addheaders = [('user-agent', 'https://github.com/nmichalov')]
    
    def start(self, start_url):
        self.crawl(start_url)
    
    def crawl(self, current_url): 
        url_parts = urlparse.urlparse(current_url)
        if url_parts.scheme == 'http':
            try:
                response = self.br.open(current_url)
            except urllib2.HTTPError, error:
                pass
            else:
                self.visited.append(current_url)
                for link in list(self.br.links()):
                    if not '@' in link.url and '?' not in link.url:
                        if link.url.startswith('http:'):
                            link = link.url
                        elif link.url.startswith('/'):
                            link = link.base_url+link.url
                        else:
                            link = link.base_url+'/'+link.url
                        if link not in self.url_list:
                            if link not in self.visited:
                                self.url_list.insert(0, link)
                            if urlparse.urlparse(link).hostname != url_parts.hostname:
                                if not self.referrer_hash.has_key(link):
                                    self.referrer_hash[link] = [current_url,]
                                else:
                                    if current_url not in self.referrer_hash[link]:
                                        self.referrer_hash[link].append(current_url)
                    else:
                        self.atypical_urls.append(link)
                    sleep(1)
        if len(self.url_list) > 0 and len(self.visited) <= self.crawl_limit:
            next_url = self.url_list.pop()
            self.crawl(next_url)
        else:
            self.report()
    
    def report(self):
        if not os.path.exists('CrawlerReports/'):
            os.mkdir('CrawlerReports/')
        url_file = open('CrawlerReports/'+self.crawler_id+'-URLFile.txt', 'a')
        for url in self.visited:
            url_file.write(url+'\n')
        url_file.close()
        atypical_file = open('CrawlerReports/'+self.crawler_id+'-AtypicalURLs.txt', 'a')
        for url in self.atypical_urls:
            atypical_file.write(str(url)+'\n')
        atypical_file.close()
        referrer_file = open('CrawlerReports/'+self.crawler_id+'-ReferrerHash.pck', 'w')
        cPickle.dump(self.referrer_hash, referrer_file)
        referrer_file.close()
                       

if __name__ == '__main__':
    start_page = raw_input('Enter starting URL: ')
    ident = raw_input('Designate an ID for this crawl: ')
    limit = int(raw_input('Enter crawl limit: '))
    NC = Crawler(ident, limit)
    NC.start(start_page)
    NC.report()
