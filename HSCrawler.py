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

    def __init__(self, crawler_id, start_url):
        self.crawler_id = crawler_id
        self.start_url = start_url
        self.out_dir =  re.sub('\/', ' SLASH ', start_url)
        self.indomain_urls = []
        self.external_urls = []
        self.visited = []
        self.br = mechanize.Browser()
        self.br.addheaders = [('user-agent', 'https://github.com/nmichalov')]
    
    def start(self):
        if not os.path.exists('Crawled/'):
            os.mkdir('Crawled')  
        os.mkdir(self.out_dir)
        self.crawl(self.start_url)
    
    def crawl(self, current_url): 
        url_parts = urlparse.urlparse(current_url)
        if url_parts.scheme == 'http':
            try:
                response = self.br.open(current_url)
            except urllib2.HTTPError, error:
                pass
            else:
                self.visited.append(current_url)
                soup = BeautifulSoup(response).prettify()
                path = re.sub('\/', ' SLASH ', url_parts.path)
                outfile = open(self.out_dir+'/'+path, 'a')
                for line in soup:
                    outfile.write(line)
                outfile.close()
                for link in list(self.br.links()):
                    if not '@' in link.url and '?' not in link.url:
                        if link.url.startswith('http:'):
                            link = link.url
                        elif link.url.startswith('/'):
                            link = link.base_url+link.url
                        else:
                            link = link.base_url+'/'+link.url
                        link_parts = urlparse.urlparse(link)
                        if link_parts.hostname == url_parts.hostname:
                            if link not in self.indomain_urls and link not in self.visited:
                                self.indomain_urls.append(link)
                        else:
                            if link.hostname not in self.external_urls:
                                self.external_urls.append(link.hostname) 
            sleep(1)
        if len(self.indomain_urls) > 0:
            next_url = self.indomain_urls.pop()
            self.crawl(next_url)
        else:
            url_file = open(out_dir+'/'+LinkedDomains, 'w')
            cPickle.dump(self.external_urls, url_file)
            url_file.close()      
        
                 
                       

if __name__ == '__main__':
    start_page = raw_input('Enter starting URL: ')
    ident = raw_input('Designate an ID for this crawl: ')
    NC = Crawler(ident, start_page)
    NC.start()
