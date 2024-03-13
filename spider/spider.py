#/usr/bin/env python

import requests
import re
import urllib.parse as urlparse

target_url = "https://thc.cybersapiens.in/"
target_links = []


def extract_links_from(url):
    response = requests.get(url)
    # Use PYTHEX to test the REGEX
    # Returns all the matches that has href="anything"
    return re.findall('(?:href=")(.*?)"', response.text) # 1st part just to find; 2nd part to return
    # response.content gets the content i.e page source of the webpage


def crawl(url):
    href_links = extract_links_from(url)
    for link in href_links:
        # joining left alone path with the original url. like /path.. http://url/path
        link = urlparse.urljoin(url, link)

        # if # thats referencing is cut out
        if "#" in link:
            link = link.split("#")[0]

        # if its no already in the list then add, and not out of bound
        if target_url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawl(link) # recursively calling to spider


crawl(target_url)