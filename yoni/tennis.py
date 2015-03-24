'''Nick has a terrible sleep schedule. He randomly picks a time between 4 AM and
6 AM to fall asleep, and wakes up at a random time between 11 AM and 1 PM of the
same day. What is the probability that Nick gets between 6 and 7 hours of
sleep?'''

import random

def toss(p):
    '''Returns True with probability p and False with probability 1-p.'''
    return random.random() < p

def length_to_k_in_a_row(p, k):
    '''Returns the length of a random coin toss sequence ending with k in a row.'''
    seq_length, latest_tosses = k, [toss(p) for _ in xrange(k)]
    num_heads = sum(1 for x in latest_tosses if x)
    #tosses = list(latest_tosses)
#    print ' '.join(map(lambda x: 'H' if x else 'T', latest_tosses)),
    while num_heads > 0 and num_heads < k:
      if latest_tosses[seq_length % k]: num_heads -= 1
      new_toss = toss(p)
      latest_tosses[seq_length % k] = new_toss
      if new_toss: num_heads += 1
#      print ('H' if new_toss else 'T'),
      #tosses.append(new_toss)
      seq_length += 1
#    print ''
    return seq_length #, tosses

#def all_equal(s):
#  return all(x == s[0] for x in s)

#def is_valid_sequence(s, k):
#  return len(s) >= k and all_equal(s[-k:]) and all(not all_equal(s[i:]) for i in xrange(len(s)-k))

def expected_length_to_k_in_a_row(p, k, sample_size=100):
  return (1.0*sum(length_to_k_in_a_row(p, k) for _ in xrange(sample_size))) / sample_size

if __name__ == '__main__':
    print length_to_k_in_a_row(0.3, 3)
#    print l, s
#    print is_valid_sequence(s, 3)

    p = 0.5
    k = 1
    #    avg_theoretical = 7
    avg_old = 0
    for n in xrange(1, 8):
        sample_size = 10**n
        avg = expected_length_to_k_in_a_row(p, k, sample_size=sample_size)
        print sample_size, avg, abs(avg-avg_old)
        avg_old = avg
