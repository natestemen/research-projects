def shuffle(n):
    left = [0]*n
    right = [1]*n
    return [a for tup in zip(left, right) for a in tup]
shuffle(100000)