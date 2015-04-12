#!/usr/bin/env python

# A man has three daughters. The product of their ages is 168, and he remembers
# that the sum of their ages is the number of trees in his yard. He counts the
# trees but cannot determine any of their ages. What are all possible ages of
# his oldest daughter?
#
# Usage:
#
# python ~/oren/problems/daughters.py <age_product> <num_daughters>
#
# In particular, to solve the puzzle run
#
# python  ~/oren/problems/daughters.py 168 3
#
# Output:
# 12,14,21

import sys, operator, itertools as it
from functools import reduce # Valid in Python 2.6+, required in Python 3

def primes(n):
  # Returns the list of primes <= n.
  s = [False] * 2 + [True] * (n-1)
  for p in xrange(2, int(n**0.5)+1):
    if s[p]:
      for x in xrange(p*p, n+1, p): s[x] = False
  return [x for x in xrange(n+1) if s[x]]

def factors(n, prime_list):
  # Returns the factors of n in non-decreasing order. Factors may be repeated.
  factor_list = []
  for p in prime_list:
    while n % p == 0:
      factor_list.append(p)
      n /= p
    if n == 1: break
  return factor_list

def divisors(factor_list):
  # Returns the set of divisors from a list of factors of n, including 1 and n.
  return set(reduce(operator.mul, factor_subset, 1)
             for m in xrange(len(factor_list)+1)
             for factor_subset in it.combinations(factor_list, m))

def age_combinations_helper(n, d, prime_list, min_age=1):
  # Generates all possible d-daughter-age tuples whose product is n.
  if n == 1:
    if min_age == 1: yield [1] * d
  elif d == 1:
    yield [n]
  else:
    for divisor in it.dropwhile(
        lambda x: x < min_age,
        it.takewhile(lambda x: x <= int(n**(1./d)),
                     sorted(divisors(factors(n, prime_list))))):
      for rest_of_factorization in \
          age_combinations_helper(n/divisor, d-1, prime_list, min_age=divisor):
        yield [divisor] + rest_of_factorization

def age_combinations(n, d):
  # Generates all possible d-daughter-age tuples whose product is n.
  return age_combinations_helper(n, d, primes(n))

def possible_ages_of_oldest(n, d):
  combinations_with_sum = {}
  for ages in age_combinations(n, d):
    unique_ages = combinations_with_sum.setdefault(sum(ages),
                                                   [set() for _ in xrange(d)])
    for i in xrange(d):
      unique_ages[i].add(ages[i])
  ambiguous = [unique_ages[d-1]
               for unique_ages in combinations_with_sum.itervalues()
               if min(len(u) for u in unique_ages) > 1]
  return set.union(*ambiguous) if ambiguous else set()

def PossibleAgesOldest_ZinovySolution(daughters, age_product):
    #First of all, regarding the problem itself, I thought about it for a long time in terms of combinations of prime factors, but never found something I was happy with. I decided to go with a direct approach, which is not necessarily all that wasteful, since many composite numbers may still be factors and limiting the range per level is also very strong. I then looked at your code and saw that you had indeed found all the prime factor combinations - very impressive. I am not sure what the speed up is - I believe it comes out to something like O(n^.5) in either case. Here is my code:
    sum_to_oldest = {}
    def Algorithm(daughters, age_product, age_sum, age_start):
        if daughters == 1:
            sum_to_oldest.setdefault(age_sum + age_product, []).append(age_product)
        else:
            for age in xrange(age_start, int(age_product ** (1. / daughters)) + 1):
                if age_product % age == 0:
                    Algorithm(daughters - 1, age_product / age, age_sum + age, age)
    Algorithm(daughters, age_product, 0, 1)
    return sorted(frozenset(it.chain(*it.ifilter(lambda v: len(v) > 1,
                                                 sum_to_oldest.itervalues()))))
  
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python %s <age_product> <num_daughters>' % (sys.argv[0],)
        sys.exit(-1)
    print ','.join(map(str, sorted(possible_ages_of_oldest(int(sys.argv[1]), int(sys.argv[2])))))
