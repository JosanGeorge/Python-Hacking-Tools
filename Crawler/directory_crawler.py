#/usr/bin/env python

import requests

def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass

target_url = "https://thc.cybersapiens.in"

with open("/root/Downloads/subdomains.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip() # strips the whitespace
        test_url = target_url + "/" + word
        response = request(test_url)
        if response:
            print("[+] Discovered Directory --> " + test_url)