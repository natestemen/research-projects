import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams.update({'font.size': 22, 'figure.figsize': (11,7), 'text.usetex': True, 'grid.linestyle': ':'})
#
# def in_shuffle(deck):
#     shuffled = []
#     halfway = len(deck) // 2
#     for i in range(len(deck)):
#         if i % 2 == 0:
#             shuffled.append(deck[halfway + i // 2])
#         else:
#             shuffled.append(deck[i // 2])
#     return shuffled
#
#
# def evolve_stack(size, option = 'in'):
#     print(size)
#     if size % 2 != 0:
#         raise ValueError('size of deck must be even')
#     initial = [1 if i < size // 2 else 0 for i in range(size)]
#     if option == 'in':
#         shuffle_type = in_shuffle
#     else:
#         shuffle_type = out_shuffle
#     shuffled = shuffle_type(initial)
#     period = 1
#     while shuffled != initial:
#         shuffled = shuffle_type(shuffled)
#         period += 1
#     return period

def card_seq(n):
	a = 1
	m = 0
	while True:
		a *= 2
		a %= (2*n + 1)
		m += 1
		if a <= 1: break
	return m

sizes = range(500000)
in_periods = [card_seq(n) for n in sizes]

with open('card_data.txt', 'w') as f:
	for i, v in enumerate(in_periods):
		f.write(str((i, v)) + '\n')

plt.scatter(sizes, in_periods, marker = '.', s = 1)
plt.title('``In Shuffles" to Return to Initial Configuration')
plt.xlabel('Number of Cards $n$')
plt.ylabel('Period $k(n)$')
plt.grid()
plt.show()
