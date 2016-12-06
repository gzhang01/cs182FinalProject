import matplotlib.pyplot as plt
import sys

file = "counts"
infile = file + ".csv"
outfile = file + ".png"

counts = []
with open(infile, "r") as f:
	counts = f.readlines()[0].split(", ")[: -1]

distribution = {}
for c in counts:
	if int(c) not in distribution:
		distribution[int(c)] = 0
	distribution[int(c)] += 1

keys = distribution.keys()

x = []
y = []

for i in xrange(min(keys) - 3, max(keys) + 4):
	x.append(i)
	try:
		y.append(distribution[i])
	except KeyError:
		y.append(0)

denom = sum(y)
y = [1.0 * i / denom for i in y]

print x
print y


plt.bar(x, y)
plt.suptitle('Distribution of Counts Over 10000 Rounds', fontsize=20)
plt.ylabel('Frequency')
plt.xlabel('Count')
plt.axis([x[0], x[-1], 0, 11.0 / 10 * max(y)])
plt.savefig(outfile)
plt.show()