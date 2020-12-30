# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def normalSearchPath(problem, fringe):
    #Insert the start node with the form like another node
    fringe.push([(problem.getStartState(), None, 0)])
    #This for the path we find out
    path = []
    #This contain the node which is visited
    visited = []

    #We check until there are no node in the fringe
    while not fringe.isEmpty():
      #Get the lasted node
      node = fringe.pop()
      #Check if it is the goal. Get node[-1] to get the lasted node
      if problem.isGoalState(node[-1][0]):
        #So it will be finished. So get out the path
        for spath in node:
          #With the form like the init. node[1] will return the direction.
           path.append(spath[1])
        #Get out of the loop
        break
      #Else check if the node is visited or not
      if not (node[-1][0] in visited):
        #If no, add it to the visited list.
        visited.append(node[-1][0])
        #Get all the successors of current node
        successors = problem.getSuccessors(node[-1][0])
        #Add it to fringe
        for item in successors:
          #In this we plus cost of path. Use for UCS.
          fringe.push(node + [(item[0],item[1],item[2]+node[-1][2])])
    
    #path[0] is the first node (Node) so remove it
    return path[1:]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    ###
    ###Idea: Check every node. When check this node, get all successors of it.
    #and add it to the stack. Ex: Visit node a, then a has 2 successors are b,c
    #so add to stack new node: (a+b) and (a+c). So everytime we check the node, we
    #use node[-1] to get the lasted node. It is an easy way to do and get the path.
    ###

    #Set fringe is a Stack
    fringe = util.Stack()
    return normalSearchPath(problem, fringe)


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    ###
    ###Idea: Check every node. When check this node, get all successors of it.
    #and add it to the queue. Ex: Visit node a, then a has 2 successors are b,c
    #so add to queue new node: (a+b) and (a+c). So everytime we check the node, we
    #use node[-1] to get the lasted node. It is an easy way to do and get the path.
    ###

    #Set fringe is a queue
    fringe = util.Queue()
    return normalSearchPath(problem, fringe)


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #This search is like another above. One thing that difference is the fringe.

    def getPrior(node):
      #Function to get the cost of one node
        return node[-1][2]
    #Set fringe is an priority queue
    fringe = util.PriorityQueueWithFunction(getPrior)
    #Get result
    return normalSearchPath(problem, fringe)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #The main things we do will be like the UCS code. Only thing that the return 
    #of the function we must plus the priority with a heuristic value.
    #This base on the fomula f(x)=g(x)+h(x) . So g(x) is item and h(x) is heuristic
    def getPrior(node):
        return node[-1][2] + heuristic(node[-1][0], problem)
    fringe = util.PriorityQueueWithFunction(getPrior)
    return normalSearchPath(problem, fringe)



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

