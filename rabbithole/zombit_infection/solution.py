#-------------------------------------------------------------------------------
# Rabbit hole - zombit_infection problem
#-------------------------------------------------------------------------------

def copy(population):
  # Returns a deep copy of the 2D population array.
  return [[cell for cell in row] for row in population]

def answer(population, x, y, strength):
  while population != new_population:
