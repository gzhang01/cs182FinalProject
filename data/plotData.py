import matplotlib.pyplot as plt
import sys

assert len(sys.argv) == 2

file = sys.argv[1]
infile = file + ".csv"
outfile = file + ".png"

lines = []
with open(infile, "r") as f:
	lines = f.readlines()
lines = [int(line.strip()) for line in lines]

color = "g"
plt.plot(lines, color)
plt.suptitle('Basic Strategy Agent (bet = 10)', fontsize=20)
plt.ylabel('Money ($)')
plt.xlabel('Iteration')
plt.savefig(outfile)
plt.show()