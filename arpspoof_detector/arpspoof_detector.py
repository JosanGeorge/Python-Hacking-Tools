#!/usr/bin/env python
import scapy.all as scapy
from scapy.layers import http
import optparse



def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


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

def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            response_mac = get_mac(packet[scapy.ARP].hwsrc)

            if real_mac != response_mac:
                print("[+] You are under ATTACK!")
        except IndexError:
            pass

interface = arguments()
sniff(interface)
