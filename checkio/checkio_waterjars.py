'''
============================================================
You stand by the edge of a lake with two empty jars. You
notice that both of the jars have a volume. You can fill
each jar with water from the lake, pour water from one jar to
the other or pour water back into lake. You should measure the volume of water in either jar. The required volume of water may be in either of the jars and it does not matter which.
Each action is described as a string of two symbols: from and to. The jars are marked as 1 and 2, the lake is marked 0. If you want to take water from the lake and fill first jar, then it's '01'. To pour water from second jar into the first would be '21'. Dump water out of the first jar and back into the lake would be '10'. When you fill a jar from the lake, that jars volume will be full. When you pour water out a jar and into the lake, that jars volume will be empty. If you pour water from one jar to another, you can only pour as much as will fill the full volume of the receiving jar.
water-jars
The function has three arguments: The volume of first jar, the volume of second jar and the goal. All arguments are positive integers (number > 0). You should return a list with action's sequence.
The solution must contain the minimum possible number of steps
Input: The volume of first jar, the volume of second jar and the goal as integers.
Output: The sequence of steps as a list/tuple with strings.
Precondition: 
0 < first, second, goal < 10
goal <= first or goal <= second
All test cases have solution.

Created on June 14, 2015
@author: Oren Livne <oren.livne@gmail.com>
============================================================
'''
import itertools as it, sys

class WaterJarSolver:
    # Breadth-first brute-force search for the optimal solution.
    _NO_SOLUTION = (sys.maxint, [])
    
    def __init__(self, a, b, goal):
        # This dictionary maps each action and jar state (a tuple (c,d), where c = #units filled in
        # first jar, d = #units filled in second jar) to the jar state after the action.
        self._actions = {
            '01': lambda c, d: (a, d),
            '02': lambda c, d: (c, b),
            '12': lambda c, d: (c - min(b - d, c), min(b, c + d)),
            '21': lambda c, d: (min(a, c + d), d - min(a - c, d)),
            '10': lambda c, d: (0, d),
            '20': lambda c, d: (c, 0)
        }
        self._goal = goal
        # Stores the optimal solution for jar states we've already solved for during the search.
        self._memo = {}

    def shortest_path_to_goal(self, key=(0, 0), states=list()):
        # Returns an optimal solution to the jar problem, starting from the jar state 'key'.
        # Output format: ({path length}, {path of moves}).
        
        # Cache states in the state space tree in the memo dictionary. Delegate to shortest_path_helper
        # for the actual calculation if we need it.
        if key not in self._memo: 
            shortest_path = self.shortest_path_helper(key, states)
            self._memo[key] = shortest_path
            return shortest_path
        return self._memo[key]

    def shortest_path_helper(self, (c, d), states):
        # Actually calculates the  optimal solution to the jar problem, starting from the jar
        # state (c,d).
        
        # If one of the jars exactly matches the goal, already done.
        if c == self._goal or d == self._goal: return (0, list())
        
        # Try all possible moves; among those that actually change the jars and lead to a jar state
        # that hasn't been encountered on the path yet (otherwise, we'd have a shorter path), find an
        # optimal one (that results in a shortest path).
        try:
            # Add the current state to the list of states we've encountered. 
            states = states + [(c, d)]
            return min(it.imap(lambda x: (len(x), x),
                               ([action] + self.shortest_path_to_goal(new_state, states)[1]
                                for action, new_state in
                                it.ifilter(lambda (_, state): state != (c, d) and state not in states,
                                           ((action, apply_action(c, d))
                                           for action, apply_action in self._actions.iteritems())))))
        except ValueError:
            # Minimum is over an empty set, i.e. no options are available.
            return WaterJarSolver._NO_SOLUTION

def checkio(a, b, goal):
    return WaterJarSolver(a, b, goal).shortest_path_to_goal()[1]

# This part is using only for self-checking and not necessary for auto-testing
def check_solution(func, initial_data, max_steps):
    a, b, goal = initial_data
    actions = {
        '01': lambda f, s: (a, s),
        '02': lambda f, s: (f, b),
        '12': lambda f, s: (
            f - (b - s if f > b - s else f),
            b if f > b - s else s + f),
        '21': lambda f, s: (
            a if s > a - f else s + f,
            s - (a - f if s > a - f else s),
        ),
        '10': lambda f, s: (0, s),
        '20': lambda f, s: (f, 0)
    }
    first, second = 0, 0
    result = func(*initial_data)
    if len(result) > max_steps:
        print('You answer contains too many steps. It can be shorter.')
        return False
    for act in result:
        if act not in actions.keys():
            print('I don''t know this action {0}'.format(act))
            return False
        first, second = actions[act](first, second)
    if goal == first or goal == second:
        return True
    print('You did not reach the goal.')
    return False

if __name__ == '__main__':
    assert check_solution(checkio, (7, 5, 6), 10), 'Example'
    assert check_solution(checkio, (8, 5, 2), 4), 'Example'
    assert check_solution(checkio, (5, 7, 6), 10), 'Example'
    assert check_solution(checkio, (3, 4, 1), 2), 'One and two'
