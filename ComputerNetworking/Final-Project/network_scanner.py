import ipaddress, socket, queue

from threadHandler import ThreadHandler
from ipScan import pingIP
from ip_prober import IpProber
from termcolor import colored


'''
FOR MY FUTURE CHANGES, CAN DISREGARD IF SEEING WHILE GRADING

TO FIX:
- local port assignment is dumb, simply copying port looking at
- max threads is an in code input dont know how to solve tho
- max threads not erroring on too many threads?? unless my compute j became mad baller

TO CHANGE?:
- commands require slashes
- rework mac scan, very ugly

TO ADD:
- connect with tcp or udp to an open port
- intro screen, account for loading of scapy
- custom timeouts
- other scan method like connect_ex
- more port scans for specific port protocols
- save scanned information
'''

# code for running help command
def helpCommand():
    print("Help: list all available commands")
    print("Usage: help\n")

    print("IpScan: Scan for any active computers in a given subnet mask.")
    print("Method: Send ICMP echo requests and remember who replies.")
    print("Usage: ipscan [mask], ex: ipscan 192.168.1.0/24\n")

    print("Connect: Connect to an ip address for further probing.")
    print("Usage: connect [ip], ex: connect 192.168.1.1\n")

    print("Quit: Quit the script.")
    print("Usage: quit")

# code for scanning ip's in given subnet
def ipScanCommand(args):
    # Validate subnet input
    if len(args) < 2:
        print("Please input subnet mask.")
        return
    subnet = args[1]
    try:
        network = ipaddress.ip_network(subnet)
        print(f"Scanning from {network[0]} to {network[-1]}.")
    except ValueError:
        print("Invalid subnet")
        return
    # preparing to thread
    ipScanThreadHandler = ThreadHandler()
    pingQ = queue.Queue()
    # starting each thread
    for ip in network:
        ipScanThreadHandler.add(pingIP, [ip, pingQ], f"Ping {ip}")
    print("All threads initialized, waiting for threads to close.")
    # wating for threads to finish
    ipScanThreadHandler.join(0)
    # displaying results
    pingReplies = list(pingQ.queue)
    pingReplies.sort()
    for ip in pingReplies:
        print(ip)
    print(f"IP scan complete. {len(pingReplies)} ip(s) found.")


# function for parsing command inputs
def parseInput(userInput):
    args = userInput.split(" ")
    if "QUIT" in args[0].upper():
        quit()
    elif "HELP" in args[0].upper():
        helpCommand()
    elif "IPSCAN" in args[0].upper():
        ipScanCommand(args)
    elif "CONNECT" in args[0].upper():
        IpProber(args)
    else:
        print(f"Unrecognized command: {args[0]}")


# Main Loop
running = True
print(colored("Welcome to Malcolm's network scanner!\n","green",attrs=["bold"]))
while running:
    userInput = input(colored("What would you like to do? (type help for command list)\n","light_blue",attrs=["bold"]))
    print(colored(f"----------Running {userInput}----------","blue"))
    try:
        parseInput(userInput)
    except Exception as e:
        print(f"Error: {e}")
    print(colored(f"---------{userInput} Complete----------","blue"))