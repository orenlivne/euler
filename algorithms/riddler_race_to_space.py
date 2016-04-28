# http://fivethirtyeight.com/features/you-have-1-billion-to-win-a-space-race-go/
import itertools as it

def russian_benefit(x):
  if x == 0: return 0
  if x == 1: return 200
  if x >= 2: return 300

def journey_time(x1, x2, x3):
  return 1600 - russian_benefit(x1) - 50*x2 - 25*x3

if __name__ == "__main__":
  # Brute-force.
  print min((journey_time(x1, x2, x3), (x1, x2, x3))
             for x1, x2, x3 in
             it.product(xrange(4), xrange(9), xrange(5))
             if 400*x1 + 150*x2 + 50*x3 <= 1000)
