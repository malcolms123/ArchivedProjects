import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import ARP, Ether, srp

'''
Co-Authored by GPT-4 for forming ARP packets
'''

def probeMAC(ip, interface):
    try:
        # Create an Ethernet frame (Layer 2) and an ARP packet (Layer 3)
        ethernet_frame = Ether(dst="ff:ff:ff:ff:ff:ff")  # Broadcast MAC address
        arp_packet = ARP(pdst=ip, op=1)  # 'op=1' indicates an ARP request
        # Combine the Ethernet frame and ARP packet
        packet = ethernet_frame / arp_packet
        # Send the packet and capture the response
        response, _ = srp(packet, iface=interface, timeout=2, verbose=False)
        # Process the response
        printed = False
        for _, received_packet in response:
            printed = True
            print(f"IP: {received_packet[ARP].psrc}, MAC: {received_packet[Ether].src}")
        if not printed:
            print("Could not connect over this interface.")
    except Exception as e:
        print("Could not connect over this interface.")