memo = {}
#
#class Collatz:
#  """Analyzes Collatz sequence lengths."""

#  def __init__(self, limit):
#    self.limit = limit

#def collatz_sequence_length(self, n):
def collatz_sequence_length(n):
  n_start = n
#    count, sequence = 1, [n]
  count = 1
  while n != 1:
    n, count = n/2 if n % 2 == 0 else (3*n+1), count + 1
    if n in memo:
#      known_length = memo[n]
#      for new_count, num in enumerate(sequence, known_length + 1):
#        memo[new_count] = num
      memo[n_start] = known_length + count
      return known_length + count
#    else:
#      sequence.append(n)
  return count

#def num_of_max_length(self):
def num_of_max_length(limit):
  max_length, max_n = 0, 0
  for n in xrange(1, limit+1):
    length = collatz_sequence_length(n)
    if length > max_length: max_length, max_n = length, n
  return max_n
#    return max((collatz_sequence_length(n), n) for n in xrange(1, limit+1))[1]

if __name__ == '__main__':
#  print Collatz(10**6).num_of_max_length()
  print num_of_max_length(10**6)
