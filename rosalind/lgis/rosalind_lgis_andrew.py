# 5 times faster and far shorter than my solution - DP
from rosalind.rosalind_lgis import read_seq

def longest_sequence_inc(l):
    inc = [(0, [])] * (len(l) + 1)
    for i in l:
        x, y = max(inc[:i])
        inc[i] = (x + 1, y + [i])
    seq = max(inc)[1]
    print ' '.join(map(str, seq))
    print len(seq)
    return seq

longest_sequence_dec = lambda a: list(reversed(longest_sequence_inc(list(reversed(a)))))

if __name__ == "__main__":
    longest_sequence_inc([9, 3, 7, 2, 4, 5, 8, 1, 10, 6])

    import time
    start_time = time.time()
    a = read_seq('rosalind_lgis3.dat')
    longest_sequence_inc(a)
    longest_sequence_dec(a)
    print time.time() - start_time, 'sec'
