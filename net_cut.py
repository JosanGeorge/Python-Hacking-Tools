#!/usr/bin/env python
# iptables -I FORWARD -j NFQUEUE --queue-num 0 (TRAPPING REQUESTS IN A QUEUE)
# iptables --flush (TO DELETE ALL THE IPTABLES *MAKE SURE TO DO THIS)

import netfilterqueue as netq

def process_packet(packet):
    print(packet)
    packet.drop()

queue = netq.NetfilterQueue()
queue.bind(0, process_packet)
queue.run