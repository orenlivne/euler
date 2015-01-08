'''
============================================================
http://projecteuler.net/problem=151

Paper sheets of standard sizes: an expected-value problem.

Problem 151
A printing shop runs 16 batches (jobs) every week and each batch requires a sheet of special colour-proofing paper of size A5.

Every Monday morning, the foreman opens a new envelope, containing a large sheet of the special paper with size A1.

He proceeds to cut it in half, thus getting two sheets of size A2. Then he cuts one of them in half to get two sheets of size A3 and so on until he obtains the A5-size sheet needed for the first batch of the week.

All the unused sheets are placed back in the envelope.


At the beginning of each subsequent batch, he takes from the envelope one sheet of paper at random. If it is of size A5, he uses it. If it is larger, he repeats the 'cut-in-half' procedure until he has what he needs and any remaining sheets are always placed back in the envelope.

Excluding the first and last batch of the week, find the expected number of times (during each week) that the foreman finds a single sheet of paper in the envelope.

Give your answer rounded to six decimal places using the format x.xxxxxx .
============================================================
'''

'''My solution, based on state-tree. I originally forgot the detail of NOT dividing by the number of batches
(expectation of #times = SUM of expectations of single times, not AVERAGE!), yet mine is much
faster than the following DP approach.'''

exp_single = lambda d: sum(p for s, p in d.iteritems() if sum(s) == 1)
def increment(d, state, p): d[state] = d.setdefault(state, 0) + p

def next_states(d):
    e = dict()
    for state, p in d.iteritems():
        sheets = sum(state)
        for i, s in ((j, t) for j, t in enumerate(state) if t):
            increment(e, cut(state, i), (p * s) / sheets)
    return e    

def exp_batches_tree(n):
    d = {tuple([1] * (n - 1)):1.0}
    e, count = exp_single(d), 1
    for _ in xrange(2, 2 ** (n - 1) - 1):
        d = next_states(d)
        e += exp_single(d)
        count += 1
    return e

def cut(state, i):
    '''Return the updated sheet count tuple obtained by the cut-in-half procedure on the sheet at position i,
     given a count sheet tuple 'state'.'''
    s = list(state)
    s[i] -= 1
    for j in xrange(i + 1, len(s)): s[j] += 1
    return tuple(s)

def E(state, memo=None):
    '''Return the expectation value of the number of times to find a single sheet in the envelope,
    starting from the count sheet tuple 'state'. Dynamic programming approach from
    http://www.haskell.org/haskellwiki/Euler_problems/151_to_160#Problem_151 with memoization
    to reduce the number of visited states.'''
    if not memo: memo = {(0,) * (len(state) - 1) + (1,) : 0.0}  # Initial condition (exclude last batch)
    sheets = sum(state)
    return memo.setdefault(state, sum((E(cut(state, i), memo=memo) * s) / sheets for i, s in enumerate(state) if s) + (sum(state) == 1))

'''Expected number of times to find a single sheet in the envelope in all batches except the
first and last, using A2..A(n-1) papers. The count tuple (state) after batch 1 is (1,...,1).'''
exp_batches_dp = lambda n: E((1,) * (n - 1))
          
if __name__ == "__main__":
    print '%.6f' % (exp_batches_dp(5),)
    for n in xrange(1, 9): print '%d %.6f' % (n, exp_batches_tree(n),)
