'''
====================================================================
Multi-level setup hierarchy.
====================================================================
'''

class Setup(object):

  def __init__(self, level_list, nu1, nu2):
    # Creates a setup with a list of levels 'level_list'. nu1 is the number of
    # cycle pre-relaxations at each level; nu2 is the number of post-relaxations.
    self.level = level_list
    self.nu1 = nu1
    self.nu2 = nu2
