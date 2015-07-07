# Submission: SUCCESSFUL. Completed in: 1 hr, 16 mins, 38 secs.

def answer(y, x):
  # If there exists an ordering such that y[i]/x[i] = const. for all i,
  # the larger the x element, the larger the corresponding y element.
  # In particular, the ratio is attained for the minimal elements of x and
  # y (as well as the maximal). Complexity: O(n) where n=len(x)=len(y).
  return int(round(100*(1 - min(y) / min(x))))

if __name__ == '__main__':
  assert answer([1.0], [1.0]) == 0
  assert answer([2.2999999999999998, 15.0, 102.40000000000001, 3486.8000000000002], [23.0, 150.0, 1024.0, 34868.0]) == 90
