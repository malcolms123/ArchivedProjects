import sys, time, random, argparse

def calculatePi(calcTime, size):
	start = time.time()
	pointsIn = 0
	ptot = 0
	while time.time() < start + calcTime:
		x = random.uniform(-size/2,size/2)
		y = random.uniform(-size/2,size/2)
		if x**2 + y**2 < (size/2)**2:
			pointsIn += 1
		ptot += 1
	Asqr = size**2
	print(f"{ptot} points sampled.")
	return Asqr*pointsIn/(ptot*(size/2)**2)

parser = argparse.ArgumentParser()
parser.add_argument("duration", help="Calculation time in seconds.", default=10, type=float)
parser.add_argument("--size", help="Size of square.", default=1, type=float)
args = parser.parse_args()


print(f"Calculating for {args.duration} seconds.")
pi = calculatePi(args.duration, args.size)
print(f"Pi ~ {pi}")



