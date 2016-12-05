import matplotlib.pyplot as plt
import sys

file = "qLearningDataQValue"
infile = file + ".csv"
outfile = file + ".png"

hit = []
stand = []
with open(infile, "r") as f:
	lines = f.readlines()
for line in lines:
	tmp = line.strip().split(", ")
	hit.append(tmp[0])
	stand.append(tmp[1])

plt.plot(hit)
plt.plot(stand)
plt.suptitle('Q Value Over Time', fontsize=20)
plt.ylabel('Q Value')
plt.xlabel('Iteration')
plt.savefig(outfile)
plt.show()