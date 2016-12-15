#-------------------------------------------------------------------------------
# Rabbit hole - zombit_infection problem
#-------------------------------------------------------------------------------

INFECTED = -1
MAX_STRENGTH = 10000

class Population(object):
  __DUMMY = MAX_STRENGTH + 1

  def __init__(self, population):
    self.__population = Population.__pad(population)

  def __eq__(self, other):
    return self.__population == other.__population

  def __ne__(self, other):
    return self.__population != other.__population

  def __repr__(self):
    return self.population().__repr__()

  def copy(self):
    # Returns a deep copy of the 2D population array.
    other = Population([[0]])
    other.__population = [row[:] for row in self.__population]
    return other

  def population(self):
    return [row[1:-1] for row in self.__population[1:-1]]

  def attempt_to_infect(self, i, j, strength):
    # Accounts for padding.
    self.__attempt_to_infect(i+1, j+1, strength)

  def spread_infection(self, strength):
    n, m = self.__size()
    for i in xrange(1, n):
      for j in xrange(1, m):
        self.__spread_infection_at(i, j, strength)

  def __spread_infection_at(self, i, j, strength):
    p = self.__population
    if p[i][j] == INFECTED:
      self.__attempt_to_infect(i-1, j, strength)
      self.__attempt_to_infect(i+1, j, strength)
      self.__attempt_to_infect(i, j-1, strength)
      self.__attempt_to_infect(i, j+1, strength)

  def __attempt_to_infect(self, i, j, strength):
    if self.__population[i][j] <= strength: self.__population[i][j] = INFECTED

  @staticmethod
  def __pad(population):
    m = len(population[0])
    d = Population.__DUMMY
    return [[d] * m] + [[d] + row + [d] for row in population] + [[d] * m]

  def __size(self):
    return len(self.__population), len(self.__population[0])

def answer(population, x, y, strength):
  p = Population(population)
  old_p = p.copy()
  p.attempt_to_infect(y, x, strength)
  while p != old_p:
    old_p = p.copy()
    p.spread_infection(strength)
  return p.population()

if __name__ == '__main__':
  assert answer([[1, 2, 3], [2, 3, 4], [3, 2, 1]], 0, 0, 2) == [[-1, -1, 3], [-1, 3, 4], [3, 2, 1]]
  assert answer([[6, 7, 2, 7, 6], [6, 3, 1, 4, 7], [0, 2, 4, 1, 10], [8, 1, 1, 4, 9], [8, 7, 4, 9, 9]], 2, 1, 5) == [[6, 7, -1, 7, 6], [6, -1, -1, -1, 7], [-1, -1, -1, -1, 10], [8, -1, -1, -1, 9], [8, 7, -1, 9, 9]]
