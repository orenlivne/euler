'''
============================================================
Solution to the foobar minion problem.
Created on May 22, 2015
@author: Oren Livne <oren.livne@gmail.com>
============================================================
'''
import random, itertools, time
from collections import OrderedDict

def best_ordering(minions):
    # Returns the minion permutation that minimizes the expected time to obtaining the password from them.
    # Runtime: O(n log n) solution for n minions.
    # Uses the observation that two consecutive minions i, i+1 can be flipped to reduce the total
    # expected time if and only if p[i]/t[i] < p[i+1]/t[i+1]. That is, we should griddy-maximize the
    # "termination-per-minute" rate.  
    t, numerator, denominator = zip(*minions)
    return sorted(range(len(t)), key=lambda i: float(numerator[i]) / (denominator[i] * t[i]), reverse=True)

def expected_time(t, q, perm):
    # Returns the expected time for a permutation perm of the minions with response times t and
    # corresponding probabilities 1-q (q is more convenient to work with here). 
    total_time = t[perm[-1]]
    for i in xrange(len(t) - 2, -1, -1):
        minion = perm[i]
        total_time = t[minion] + q[minion] * total_time
    return total_time  

def best_ordering_brute_force(minions):
    # Returns the minion permutation that minimizes the expected time to obtaining the password from them.
    # Runtime: n! solution for n minions (brute force).
    t, numerator, denominator = zip(*minions)
    q, n = [1 - float(x) / y for x, y in zip(numerator, denominator)], len(t)
    return list(min((expected_time(t, q, perm), perm) for perm in itertools.permutations(xrange(n)))[1])

def generate_test_case(n, max_int=1024):
    # Generates a random list of times t[i] and probabilities (p[i] = numerator[i]/denominator[i]) for
    # Returns t, numerator, denominator.
    t = [random.randint(1, max_int) for _ in xrange(n)]
    numerator = [random.randint(1, max_int) for _ in xrange(n)]
    # Ensure that p[i] <= 1.
    denominator = [random.randint(x, max_int) for x in numerator]
    return zip(t, numerator, denominator)

def run_random_validation_tests(max_num_minions=7, num_tests=1000):
    # Run random testing of fast method against brute force and validate that the agree.
    for n in xrange(1, max_num_minions + 1):
        print 'Testing with %d minions...' % (n,)
        for _ in xrange(num_tests):
            minions = generate_test_case(n)
            # The fast may not agree with brute force up to round-off errors if there are multiple
            # minimizers. Thus, check that both methods give the same minimum expected time, which must
            # be unique.
            t, numerator, denominator = zip(*minions)
            q = [1 - float(x) / y for x, y in zip(numerator, denominator)]
            y = expected_time(t, q, best_ordering_brute_force(minions))
            x = expected_time(t, q, best_ordering(minions))
            if abs(x - y) > 1e-10 * abs(x):
                t, numerator, denominator = zip(*minions)
                q, n = [1 - float(x) / y for x, y in zip(numerator, denominator)], len(t)
                print 'Found difference between brute force and fast methods!'    
                print minions
                print best_ordering(minions), x
                print best_ordering_brute_force(minions), y
            assert(abs(x - y) < 1e-10 * abs(x))

def run_timing_tests(methods, max_num_minions=7, num_tests=1000):
    # Times the methods in the dictionary (label, method functor) against each other for increasingly
    # more minion numbers.
    methods = OrderedDict(methods)
    for n in xrange(1, max_num_minions + 1):
        total_time = [0] * len(methods)
        for _ in xrange(num_tests):
            minions = generate_test_case(n)
            for i, method in enumerate(methods.itervalues()):
                t = time.time() 
                method(minions)
                total_time[i] += (time.time() - t)
        print '%d minions:' % (n,),
        for label, t in zip(methods.iterkeys(), total_time):
            print '\t%s: %8.2e s' % (label, t / num_tests),
        print ''

if __name__ == '__main__':
    # foobar examples.
    assert(best_ordering([[5, 1, 5], [10, 1, 2]]) == [1, 0])
    assert(best_ordering([[390, 185, 624], [686, 351, 947], [276, 1023, 1024], [199, 148, 250]]) == [2, 3, 0, 1])

    # Generate random test cases, validate and time the fast method against brute force.
    run_random_validation_tests()
    run_timing_tests([('Brute force', best_ordering_brute_force), ('Fast', best_ordering)])
