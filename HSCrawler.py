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
from BeautifulSoup import BeautifulSoup
from time import sleep

class Crawler:

    def __init__(self, start_url):  
        self.start_url = start_url
        self.indomain_urls = []
        self.external_urls = []
        self.visited = []
        self.br = mechanize.Browser()
        self.br.addheaders = [('user-agent', 'https://github.com/nmichalov')]
    
    def start(self):
        cur_dir = os.getcwd()
        page_dir = urlparse.urlparse(self.start_url).netloc
        out_dir = cur_dir+'/'+page_dir
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        self.crawl(self.start_url, out_dir)

    def crawl(self, current_url, out_dir): 
        current_url_parts = urlparse.urlparse(current_url)
        try:
            response = self.br.open(current_url)
        except urllib2.HTTPError, error:
            pass
        else:
            self.visited.append(current_url)
            soup = BeautifulSoup(response).prettify()
            page_file = re.sub('\/', ' SLASH ', current_url_parts.netloc+current_url_parts.path)
            outfile = open(out_dir+'/'+page_file, 'a')
            for line in soup:
                outfile.write(line)
            outfile.close()
            for link in list(self.br.links()):
                if '@' not in link.url and '?' not in link.url and '#' not in link.url:
                    if link.url.startswith('http:'):
                        if link.url not in self.external_urls:
                            self.external_urls.append(link.url)
                    else:
                        link = 'http://'+current_url_parts.netloc+link.url
                        if link not in self.visited and link not in self.indomain_urls:
                            self.indomain_urls.append(link)
            sleep(1)
        print self.indomain_urls
        print
        print self.visited
        print
        print '---------------'
        print
        if len(self.indomain_urls) > 0:
            next_url = self.indomain_urls.pop()
            self.crawl(next_url, out_dir)
        else:
            url_file = open(out_dir+'/ExternalLinkeds', 'w')
            cPickle.dump(self.external_urls, url_file)
            url_file.close()      
        
                 
                       

if __name__ == '__main__':
    start_page = raw_input('Enter starting URL: ')
    NC = Crawler(start_page)
    NC.start()
