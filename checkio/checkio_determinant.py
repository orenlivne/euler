def checkio(data):
  return data[0][0] if len(data) == 1 else sum((1 if col % 2 == 0 else -1) * data[0][col] * checkio([data[row][:col] + data[row][col+1:] for row in xrange(1, len(data))]) for col in xrange(len(data)))

#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
  print checkio([[4, 3], [6, 3]])
  assert checkio([[4, 3], [6, 3]]) == -6, 'First example'

  assert checkio([[1, 3, 2],
                  [1, 1, 4],
                  [2, 2, 1]]) == 14, 'Second example'
