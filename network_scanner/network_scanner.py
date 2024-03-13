#!/usr/bin/env python3
import scapy.all as scapy
import argparse

def argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Specify The IP Address Or The IP Range")
    options = parser.parse_args()
    if not options.target:
        print("Specify The IP, --help for more info")
    else:
        return options

def scan(ip):
    arp_req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_broadcast = broadcast / arp_req
    answered = scapy.srp(arp_req_broadcast, timeout=1, verbose=False)[0]

    client_list = []
    for element in answered:
        client_dict = {"IP":element[1].psrc, "MAC":element[1].hwsrc}
        client_list.append(client_dict)
    return client_list

def print_result(print_value):
    print("________________________________________________________________")
    print("  IP Address\t\t\t   MAC Address\n----------------------------------------------------------------")
    for client in print_value:
        print(client["IP"] + "\t\t\t" + client["MAC"])

ip = argument()
scan_result = scan(ip.target)
print_result(scan_result)