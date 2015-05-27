'''
============================================================
Given a+b and a XOR b, what is the number of distinct
ordered pairs (a,b) of positive integers?

Created on May 26, 2015
@author: Oren Livne <oren.livne@gmail.com>
============================================================
'''
import random, time

def num_digits(x):
    count = 0
    while x: count, x = count + 1, x / 2
    return count

def xor_pairs(s, x):
    # Returns the number of ordered pairs (a,b) with s = a + b and x = a ^ b.
    # Runtime complexity: O(log s).
    print 'xor_pairs(%d,%d)' % (s, x)
    if s == 0:
        num_solutions = 1 if x == 0 else 0
        print 'xor_pairs(%d,%d) = %d' % (s, x, num_solutions) 
        return num_solutions
    if x == 0:
        num_solutions = 1 if s % 2 == 0 else 0
        print 'xor_pairs(%d,%d) = %d' % (s, x, num_solutions)
        return num_solutions
    num_s_digits, num_x_digits = num_digits(s), num_digits(x)
    closest_two_power = 1 << (num_s_digits - 1)
    print '#s', num_s_digits, '#x', num_x_digits, 'closest_two_power', closest_two_power
    if num_x_digits == num_s_digits:
        num_solutions = 2 * xor_pairs(s - closest_two_power, x - closest_two_power)
    else:
        num_solutions = xor_pairs(s - closest_two_power, x - (1 << (num_x_digits - 1)))
    print 'xor_pairs(%d,%d) = %d' % (s, x, num_solutions)
    return num_solutions

def xor_pairs_brute_force(s, x):
    # Returns the number of ordered pairs (a,b) with s = a + b and x = a ^ b using brute force.
    # Runtime complexity: O(s).
    return sum(1 for a in xrange(s + 1) if a ^ (s - a) == x)

def run_random_validation_tests(max_s=100):
    # Runs random testing of fast method against brute force and validate that the agree.
    for s in xrange(max_s + 1):
        for x in xrange(2 * s):  # a ^ b cannot have more digits than a + b.
            print '-' * 80
            print 's', s, 'x', x, 'bf', xor_pairs_brute_force(s, x)  # , xor_pairs(s, x)
            assert(xor_pairs(s, x) == xor_pairs_brute_force(s, x))
            
#         print 'Testing with %d minions...' % (n,)
#         for _ in xrange(num_tests):
#             minions = generate_test_case(n)
#             # The fast may not agree with brute force up to round-off errors if there are multiple
#             # minimizers. Thus, check that both methods give the same minimum expected time, which must
#             # be unique.
#             t, numerator, denominator = zip(*minions)
#             q = [1 - float(x) / y for x, y in zip(numerator, denominator)]
#             y = expected_time(t, q, best_ordering_brute_force(minions))
#             x = expected_time(t, q, best_ordering(minions))
#             if abs(x - y) > 1e-10 * abs(x):
#                 t, numerator, denominator = zip(*minions)
#                 q, n = [1 - float(x) / y for x, y in zip(numerator, denominator)], len(t)
#                 print 'Found difference between brute force and fast methods!'    
#                 print minions
#                 print best_ordering(minions), x
#                 print best_ordering_brute_force(minions), y
#             assert(abs(x - y) < 1e-10 * abs(x))

# def run_timing_tests(methods, max_num_minions=7, num_tests=1000):
#     # Times the methods in the dictionary (label, method functor) against each other for increasingly
#     # more minion numbers.
#     methods = OrderedDict(methods)
#     for n in xrange(1, max_num_minions + 1):
#         total_time = [0] * len(methods)
#         for _ in xrange(num_tests):
#             minions = generate_test_case(n)
#             for i, method in enumerate(methods.itervalues()):
#                 t = time.time() 
#                 method(minions)
#                 total_time[i] += (time.time() - t)
#         print '%d minions:' % (n,),
#         for label, t in zip(methods.iterkeys(), total_time):
#             print '\t%s: %8.2e s' % (label, t / num_tests),
#         print ''

if __name__ == '__main__':
    # assert(xor_pairs_brute_force(10, 4) == 2)  # (3,7), (7,3)
    # assert(xor_pairs(10, 4) == 2)  # (3,7), (7,3)
    
    # assert(xor_pairs(100, 90) == 16)  # (3,7), (7,3)

    # Generate random test cases, validate and time the fast method against brute force.
    run_random_validation_tests()
    # run_timing_tests([('Brute force', best_ordering_brute_force), ('Fast', best_ordering)])
