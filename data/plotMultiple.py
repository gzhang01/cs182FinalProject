import matplotlib.pyplot as plt
import sys

assert len(sys.argv) >= 2

files = []

for i in xrange(1, len(sys.argv) - 1):
	files.append(sys.argv[i])

infiles = [file + ".csv" for file in files]
outfile = sys.argv[-1]

lines = []
for infile in infiles:
	with open(infile, "r") as f:
		tmp = f.readlines()
	tmp = [int(line.strip()) for line in tmp]
	lines.append(tmp)

for line in lines:
	plt.plot(line)
plt.suptitle('Performance of Multiple Agents (bet = 10)', fontsize=20)
plt.ylabel('Money ($)')
plt.xlabel('Iteration')
plt.savefig(outfile)
plt.show()