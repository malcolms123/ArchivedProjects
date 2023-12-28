import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

import sys
from scapy.all import *

'''
Co-Authored by GPT-4 for finding window size in TCP syn/ack packet
'''

def os_fingerprint(target_ip, port):
    # Send a SYN packet with a specific window size
    syn_packet = IP(dst=target_ip) / TCP(sport=RandShort(), dport=port, flags='S', window=5840)
    syn_ack_packet = sr1(syn_packet, timeout=5, verbose=0)

    if syn_ack_packet is None:
        print("No response. Make sure port is open to TCP connections.")
        return

    # Check the received packet's flags and window size
    if syn_ack_packet[TCP].flags == 'SA':
        window_size = syn_ack_packet[TCP].window
        os = identify_os(window_size)
        print(f"Likely OS: {os}")
    else:
        print("Unexpected response. Make sure port is open to TCP connections.")
        return

def identify_os(window_size):
    # values found online and experimentally
    os_dict = {
        4128: "iOS",
        5720: "Google",
        5840: "Linux (Kernel 2.6+)",
        8192: "Windows",
        64240: "Linux",
        65392: "Windows",
        65535: "MacOS"
    }

    return os_dict.get(window_size, "Unknown")
