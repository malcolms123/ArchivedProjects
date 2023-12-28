import ipaddress, queue, tqdm, time

from threadHandler import ThreadHandler
from ping3 import ping
from portScan import udpScan, tcpScan
from termcolor import colored

# class to handle sub program that runs when connected to an ip
class IpProber:

	def __init__(self, args):
		# validating ip input
		if len(args) < 2:
			print("Please input IP address.")
			return
		try:
			ipaddress.ip_address(args[1])
			self.ip = args[1]
		except:
			print("Invalid IP address.")
			return
		# setting all constants
		self.ip = args[1]
		self.udpTimeout = 1
		self.tcpTimeout = 1
		# main loop
		self.connected = True
		while self.connected:
			userInput = input(colored("What would you like to do? (type help for command list)\n","cyan"))
			print(colored(f"----------Running {userInput}----------","yellow"))
			try:
				self.parseConnectedInput(userInput)
			except Exception as e:
				print(f"Error: {e}")
			print(colored(f"---------{userInput} Complete----------","yellow"))

	# function for parsing command input
	def parseConnectedInput(self, userInput):
		args = userInput.split(" ")
		if "DISCONNECT" in args[0].upper():
			self.connected = False
		elif "HELP" in args[0].upper():
			self.helpConnectedCommand()
		elif "PING" in args[0].upper():
			self.pingCommand()
		elif "MAC" in args[0].upper():
			self.macConnectedCommand(args)
		elif "UDP" in args[0].upper():
			self.udpConnectedCommand(args)
		elif "TCP" in args[0].upper():
			self.tcpConnectedCommand(args)
		elif "OS" in args[0].upper():
			self.osFingerprintConnectedCommand(args)
		else:
			print(f"Unrecognized command: {args[0]}")

	# function for printing help
	def helpConnectedCommand(self):
		print("Help: list all available commands")
		print("Usage: help\n")

		print("MAC: Get the MAC address of a given ip.")
		print("Method: Broadcast ARP request for the ip and get the MAC from the ARP response.")
		print("Usage: mac [interface], ex: mac en0\n")

		print("UDP: probe a selected range of ports for UDP services.")
		print("Method: Send a UDP packet to ports and listen for a response.")
		print("Usage: udp [start_port] [end_port], ex: udp 0 65535\n")

		print("TCP: probe a selected range of ports for TCP services.")
		print("Method: Send a TCP SYN to ports and listen for SYN ACK responses.")
		print("Usage: tcp [start_port] [end_port], ex: tcp 0 65535\n")

		print("OS: Try to get the operating system through an open TCP port.")
		print("Method: Establish a TCP connection and try to match window size to an operating system.")
		print("Usage: os [tcp_port], ex: os 12345\n")

		print("Disconnect: Disconnect from IP.")
		print("Usage: disconnect")

	# function for pinging computer
	def pingCommand(self):
		rtt = ping(self.ip)
		if rtt is not None:
			print(f"Ping time: {round(rtt*1000,2)} ms.")

	# function for verifying inputted ports
	def checkPortBounds(self, args):
		if len(args) < 3:
			print("Please input port boundaries.")
			return
		try:
			start_port = int(args[1])
			end_port = int(args[2])
		except:
			print("Ports must be integers.")
			return
		if start_port > end_port or end_port > 65535 or start_port < 0:
			print("Invalid ports.")
			return
		return range(start_port, end_port+1)

	def udpConnectedCommand(self, args):
		# check validity
		scanRange = self.checkPortBounds(args)
		if scanRange is None: return
		# initialize helpers
		udpQ = queue.Queue()
		udpProbeThreadHandler = ThreadHandler()
		# start threads
		for port in tqdm.tqdm(scanRange):
			loPort = port
			udpProbeThreadHandler.add(udpScan,[self.ip,port,loPort,udpQ,self.udpTimeout],f"UDP Scan {self.ip}|{port}")
		# wait for completion
		print("All threads initialized, waiting for threads to close.")
		udpProbeThreadHandler.join(1)
		# displaying results
		udpReplies = list(udpQ.queue)
		udpReplies.sort()
		for port in udpReplies:
		    print(port)
		print(f"UDP probe complete. Found {len(udpReplies)} open ports.")

	def tcpConnectedCommand(self, args):
		# check validity
		scanRange = self.checkPortBounds(args)
		if scanRange is None: return
		# initialize helpers
		tcpQ = queue.Queue()
		tcpProbeThreadHandler = ThreadHandler()
		# start threads
		for port in tqdm.tqdm(scanRange):
			loPort = port
			tcpProbeThreadHandler.add(tcpScan,[self.ip,port,loPort,tcpQ,self.tcpTimeout],f"UDP Scan {self.ip}|{port}")
		# wait for completion
		print("All threads initialized, waiting for threads to close.")
		tcpProbeThreadHandler.join(1)
		# displaying results
		tcpReplies = list(tcpQ.queue)
		tcpReplies.sort()
		for port in tcpReplies:
		    print(port)
		print(f"TCP probe complete. Found {len(tcpReplies)} open ports.")

	# function for checking mac address
	def macConnectedCommand(self, args):
		# importing here because scapy library takes a second to initialize
		from macScan import probeMAC
		if len(args) < 2:
			print("Please input network interface.")
			return
		probeMAC(self.ip, args[1])

	# function for OS fingerprinting
	def osFingerprintConnectedCommand(self, args):
		# importing here because scapy library takes a second to initialize
		from osFingerprint import os_fingerprint
		if len(args) < 2:
			print("Please give open TCP port.")
			return
		try:
			port = int(args[1])
			if not (port > 0 and port < 65535):
				print("Invalid port.")
				return
		except:
			print("Invalid port.")
			return
		os_fingerprint(self.ip, port)

















