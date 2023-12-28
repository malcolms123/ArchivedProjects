import queue
from ping3 import ping

# threadable ping function for ipscan
def pingIP(ip,q,debug=False):
	try:
		rtt = ping(str(ip))
		if rtt is not None:
			q.put(ip)
	except Exception as e:
		if debug:
			print(f"Error pinging {ip}: {e}")

