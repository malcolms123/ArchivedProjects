import socket

from termcolor import colored

# scan if port responds to UDP
def udpScan(ip, port, loPort, q, timeout, debug=False):
    try:
        # prepare local socket
        udpSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        udpSocket.bind(('0.0.0.0', loPort))
        udpSocket.settimeout(timeout)
        # send data to target socket
        dummyString = "THIS IS DUMMY DATA THIS IS DUMMY DATA"
        udpSocket.sendto(dummyString.encode(), (ip, port))
        # wait for a response
        data,caddress = udpSocket.recvfrom(4096)
        udpSocket.close()
        # saving port as active
        q.put(port)
    except Exception as e:
        if e.errno == 24:
            print(colored("ERROR TOO MANY THREADS, DECREASE MAX THREAD COUNT","red",attrs=["bold"]))
        if debug:
            if str(e) != "timed out":
                print(f"Error udp scanning {ip}|{port}: {e}")

# scan if port will syn/ack a TCP syn packet
def tcpScan(ip, port, loPort, q, timeout, debug=False):
    try:
        # prepare local socket
        tcpSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        tcpSocket.settimeout(timeout)
        # attempt to connect to target socket
        tcpSocket.connect((ip, port))
        tcpSocket.close()
        # save response
        q.put(port)
    except Exception as e:
        if e.errno == 24:
            print(colored("ERROR TOO MANY THREADS, DECREASE MAX THREAD COUNT","red",attrs=["bold"]))
        if debug:
            if str(e) != "timed out":
                print(f"Error tcp scanning {ip}|{port}: {e}")



















