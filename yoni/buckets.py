'''
What is the probability of an empty bucket after n objects are dropped into
k buckets (each object dropped into buckets with uniform probability)?

Problem arising in IMF from karir@.

Document: go/empty-drop-uniform-bucket-prob
'''

import random, math, itertools as it, numpy as np, matplotlib.pyplot as P
from scipy.special import binom

def toss(p):
    '''Returns True with probability p and False with probability 1-p.'''
    return random.random() < p

def num_nonempty_buckets(k, n):
  # Returns the number of non-empty buckets after n objects are uniformly
  # randomly dropped into one of k buckets.
  buckets = [0] * k
  for _ in xrange(n): buckets[int(k * random.random())] += 1
#  print buckets, sum(1 for bucket in buckets if bucket > 0)
  return sum(1 for bucket in buckets if bucket > 0)

def sampling_is_nonempty_bucket(k, n, sample_size=100):
  return float(sum(1 for _ in 
                   it.ifilter(lambda x: x < k, 
                              (num_nonempty_buckets(k, n) 
                               for _ in xrange(sample_size)))))/sample_size

def log_factorial(k):
  # Returns [log(0!),...,log(k!)]. Note that log(i!) = sum_{j=0}^i log(j),
  # allowing a simple dynamic programming to calculate the array in O(k).
  l = [0] * (k+1)
  for i in xrange(2, k+1): l[i] = l[i-1] + math.log(i)
  return l

def theoretical_is_nonempty_bucket(k, n, debug=False):
  if n < k: return 1
  p, s = 0.0, 1
  l = log_factorial(k)
  for i in xrange(1, k):
    term = s * math.exp(l[k] - l[k-i] - l[i] + n * math.log(float(k-i)/k))
    if debug: print 'i', i, term
    if abs(term) <= 1e-15: break
    p += term
    s *= -1
  return p

def compare_theoretical_and_sampling(k, num_ratios=50):
  for ratio in np.linspace(0, 3, num=num_ratios):
    k_critical = k * math.log(k)
    n = int(k_critical * ratio)
    p_theoretical = theoretical_is_nonempty_bucket(k, n)
    p_sampling = sampling_is_nonempty_bucket(k, n)
    print 'k', k, 'n', n, p_theoretical, p_sampling, abs(p_theoretical - p_sampling)

def plot_theoretical_sampling_prob_comparison(num_ratios=50, sample_size=100, k_max=3):
  r = np.linspace(0, 3, num=num_ratios)
  K = 4 ** np.arange(1, k_max + 1)
  P.figure(1)
  P.clf()
  P.hold(True)
  for k, c in it.izip(K, it.cycle(['k', 'r', 'b', 'g', 'm'])):
    print 'k', k
    N = map(int, k * math.log(k) * r)
    P.plot(r, [theoretical_is_nonempty_bucket(k, n) for n in N], '%s-' % (c,), \
           r, [sampling_is_nonempty_bucket(k, n, sample_size=sample_size) for n in N], '%s--' % (c,))
  P.grid(True)
  P.legend(list(it.chain.from_iterable(('%d buckets, theoretical' % (k,), '%d buckets, theoretical' % (k,)) for k in K)))
  P.xlabel('n / (k log k)')
  P.ylabel('p(n,k)')
  P.title('Probability of an Empty Bucket After Dropping n Objects to $k$ Buckets')
  P.show()
  P.savefig('buckets_comparison.png')

def plot_theoretical_prob(num_ratios=50, k_max=5):
  r = np.linspace(0, 3, num=num_ratios)
  K = 2 ** np.arange(1, k_max + 1)
  P.figure(1)
  P.clf()
  P.hold(True)
  for k, c in it.izip(K, it.cycle(['k', 'r', 'b', 'g', 'm'])):
    print 'k', k
    N = map(int, k * math.log(k) * r)
    P.plot(r, [theoretical_is_nonempty_bucket(k, n) for n in N], '%s-' % (c,))
  P.grid(True)
  P.legend(['%d buckets' % (k,) for k in K])
  P.xlabel('n / (k log k)')
  P.ylabel('p(n,k)')
  P.title('Theoretical Probability of an Empty Bucket After Dropping n Impressions to $k$ Buckets')
  P.show()
  P.savefig('buckets_theoretical.png')

def k_sequence(factor=1.1):
  k = 1
  while True:
    yield k
    k = max(int(1.1*k), k + 1)

def take_while_prob_le(K, n, p_threshold):
  # Return the curve (k, p(n,k)) for a fixed n, starting from k=1 and increasing
  # it while p <= p_threshold.
  return zip(*list(
      it.takewhile(lambda (k, p): p <= p_threshold, 
                   ((float(k), theoretical_is_nonempty_bucket(k, n))
                    for k in K))))

def approximate_is_nonempty_bucket(k, n):
  return k * (1 - 1.0 / k) ** n

def plot_theoretical_approximate_prob_comparison(num_k_points=100, factor=1.1, n_max=3, p_threshold=0.1):
  # Plots the approximation (3) vs. the exact probability in the range n > n* = k*log(k).
  N = 100 * 10 ** np.arange(0, n_max + 1)
  P.figure(1)
  P.clf()
  P.hold(True)
  for n, c in it.izip(N, it.cycle(['k', 'r', 'b', 'g', 'm'])):
    print 'n', n
    K_initial = map(int, np.linspace(1, n, num_k_points))
    K, p = take_while_prob_le(K_initial, n, p_threshold)
    p_approx = np.array([approximate_is_nonempty_bucket(k, n) for k in K])
    K, p = np.array(K), np.array(p)
    K_scaled = K * (math.log(n) / n)
#    print np.array(zip(K_scaled, p, p_approx))
    P.semilogy(K_scaled, p, '%s-' % (c,), K_scaled, p_approx, '%s--' % (c,))
  P.grid(True)
  P.legend(list(it.chain.from_iterable(('%d impressions, theoretical' % (n,), '%d impressions, approximate' % (n,)) for n in N)), loc='best', fontsize=8)
  P.xlim([0, 1])
  P.ylim([10 ** -10, p_threshold])
  P.xlabel('Buckets per Impression (k / (n / log(n)))')
  P.ylabel('p(n,k)')
  P.title('Probability of an Empty Bucket After Dropping n Objects to $k$ Buckets')
  P.show()
  P.savefig('buckets_vs_k.png')

if __name__ == '__main__':
  plot_theoretical_approximate_prob_comparison(num_k_points=1000, factor=1.01, n_max=4, p_threshold=0.1)
#  plot_theoretical_sampling_prob_comparison(num_ratios=50, sample_size=200, k_max=3)
#  plot_theoretical_prob(num_ratios=100, k_max=6)
#  print theoretical_is_nonempty_bucket(30, int(2*30*math.log(30)), debug=True)
