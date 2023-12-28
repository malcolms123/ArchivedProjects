from prettytable import PrettyTable
import argparse


class TraceIn:
	def __init__(self, bytedata):
		self.SWID = bytedata[0:2]
		self.LnkID = bytedata[2:4]
		self.DESTMAC = self.formatMAC(bytedata[4:16])
		self.SRCMAC = self.formatMAC(bytedata[16:28])

	def formatMAC(self,macData):
		s = f"{macData[0:2]}-{macData[2:4]}-{macData[4:6]}-{macData[6:8]}-{macData[8:10]}-{macData[10:12]}"
		return s

class TraceOut:
	def __init__(self, data):
		self.SWID = data[0]
		self.LnkID = data[1]
		self.DESTMAC = data[2]
		self.SRCMAC = data[3]
		self.OutLnk = data[4]


parser = argparse.ArgumentParser()
parser.add_argument("trace", help="Trace to process.")
parser.add_argument("-s", action="store_true", help="Calculate link statistics.", default=False)
parser.add_argument("-d", action="store_true", help="Show network diagram.", default=False)
args = parser.parse_args()


trace_file = args.trace
chunkSize = 14

received = []
with open(trace_file,'rb') as file:
	while True:
		chunk = file.read(chunkSize)
		if not chunk:
			break
		tIn = TraceIn(chunk.hex())
		received.append(tIn)


outDict = {}
links = []
linksIn = []
linksOut = []
outTable = PrettyTable()
outTable.field_names = ["SWID","LnkID","DESTMAC","SRCMAC","OutLnk"]
for trace in received:
	# remember/update what link srcmac is on
	outDict[trace.SRCMAC] = trace.LnkID
	# remember link exist, only include known links (must receive trace from)
	if links.count(trace.LnkID) == 0:
		links.append(trace.LnkID)
	# check if known destination
	if trace.DESTMAC in outDict:
		found = outDict[trace.DESTMAC]
		# check if destination is source
		if found == trace.LnkID:
			outLnk = "DROP"
		else:
			outLnk = found

	else: outLnk = "ff"
	linksIn.append(trace.LnkID)
	linksOut.append(outLnk)
	outTable.add_row([trace.SWID,trace.LnkID,trace.DESTMAC,trace.SRCMAC,outLnk])

print(outTable)


if args.s:
	broadcasts = linksOut.count("ff")
	rxs = [0]*len(links)
	txs = [0]*len(links)
	for idx in range(len(links)):
		rxs[idx] = linksIn.count(links[idx])
		txs[idx] = linksOut.count(links[idx]) + broadcasts

	linkTable = PrettyTable()
	linkTable.field_names = ["Link","RX","TX"]
	rxt = sum(rxs)
	txt = sum(txs)
	for idx in range(len(links)):
		linkTable.add_row([links[idx],f"{rxs[idx]} ({round(100*rxs[idx]/rxt,1)}%)",f"{txs[idx]} ({round(100*txs[idx]/txt,1)}%)"])
	print(linkTable)


if args.d:
	linkMACs =[[] for _ in range(len(links))]
	for mac in outDict:
		link = outDict[mac]
		idx = links.index(link)
		if linkMACs[idx].count(mac) == 0:
			linkMACs[idx].append(mac)
	for idx in range(len(links)):
		s = ""
		for mac in linkMACs[idx]:
			s += mac + ", "
		s = s[:-2]
		print(f"{links[idx]} => {s}")




