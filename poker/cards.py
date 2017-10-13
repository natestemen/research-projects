import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams.update({
	'font.size': 22,
	'figure.figsize': (11,7),
	'text.usetex': True,
	'grid.linestyle': ':'
})

def card_seq(n):
	a = 1
	m = 0
	while True:
		a *= 2
		a %= (2*n + 1)
		m += 1
		if a <= 1: break
	return m

max_size = 100000
sizes = range(max_size)
in_periods = [card_seq(n) for n in sizes]

with open('card_data.txt', 'w') as f:
	for i, v in enumerate(in_periods):
		f.write(str((i, v)) + '\n')

# plt.scatter(sizes, in_periods, marker = '.', s = 1)
# plt.title('In Shuffles" to Return to Initial Configuration')
# plt.xlabel('Number of Cards $n$')
# plt.ylabel('Period $k(n)$')
# plt.grid()
# plt.show()
