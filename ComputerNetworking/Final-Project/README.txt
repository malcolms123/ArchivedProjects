This project is a network scanner that lets the user scan their current network.
In order to send certain packets (ICMP, ARP) the program must be ran with 'sudo' permissions.

	usage: sudo python3 network_scanner.py

Once the software is running the user is put into a terminal where they can scan a specified subnet mask.

	command: ipscan [mask], ex. ipscan 192.168.1.0/24
	method: Sends ICMP ping packets to all IPs, remembering which respond.

All computers that respond to an ICMP ping are then listed
These computers can be connected to 

	command: connect [ip], ex. connect 192.168.1.1
	method: Doesn't really do anything except prime the software to send to a specific IP address.

Once connected to the user can:
	- ping the computer

		command: ping
		method: ICMP ping packet, measure round trip time.

	- get the MAC address of the computer

		command: mac [interface], ex. mac en0
		method: Broadcast ARP request packet for the connected IP address.

	- scan for active UDP ports

		command: udp [low_port] [high_port], ex. udp 0 65535
		method: Send UDP dummy data remembering which ports respond.

	- scan for active TCP ports

		command: tcp [low_port] [high_port], ex. tcp 0 65535
		method: Send TCP SYN packets remembering which ports SYN ACK.

	- os fingerprint the computer

		command: os [tcp_port], ex. os 1234
		method: Send TCP SYN packets, comparing response SYN ACK window size and compare to list of known values.