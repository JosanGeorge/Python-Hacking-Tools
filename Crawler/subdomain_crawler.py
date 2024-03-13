#/usr/bin/env python

import requests

def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass

target_url = "google.com"

with open("dns.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip() # strips the whitespace
        test_url = word + "." + target_url
        response = request(test_url)
        if response:
            print("[+] Discovered Subdomain --> "+ test_url)
