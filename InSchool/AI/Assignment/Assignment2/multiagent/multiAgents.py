# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        """This function will return the evaluation of an action come from
        the getAction function. This evaluation is based on the distance to the food
        and the distance to the agent. The higher is better.
        """

        #Get list remain food to check the distance to each.
        listRemainFoods = newFood.asList()
        #Get number of food remain to know if it complete.
        numRemainFoods = len(listRemainFoods)
        #getAction will get the highest score and the nearest distance. So set 
        #distane as a very high number and score is a very smaill number
        retScore = -1e4
        calDistance = 1e4

        #No food mean the game will be completed
        if numRemainFoods == 0:
          #Distance set to 0, so the return score will be the hightest
          calDistance = 0
        else:
          #Caculate the distan betten the newPos and each food. Get the nearest food.
          for i in range(numRemainFoods):
            #Caculate the distance, numRemainFoods*100 to make sure that work for is situation
            #       food
            #       agent
            #so if don't add it, agent will valuate 4 direction like the one.
            tempDistance = manhattanDistance(listRemainFoods[i], newPos) + numRemainFoods*100
            #Get the smaller distance
            if tempDistance < calDistance:
              calDistance = tempDistance
        
        #Get the score base on the distance
        retScore = -calDistance

        #Check if the new pos can be met a ghost
        for i in range(len(newGhostStates)):
          oneGhostPos = successorGameState.getGhostPosition(i+1)
          if manhattanDistance(newPos, oneGhostPos) <= 1:
            #meet ghost, so the return score is very min.
            retScore = -1e4

        return retScore
            

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        #Data get from the MultiAgentSearchAgent class
        #Number of agent in the map
        numNowAgents = gameState.getNumAgents()
        ActionScore = []

        def recursion(inState, inHeight):
          if inHeight >= self.depth*numNowAgents or inState.isWin() or inState.isLose():
            return self.evaluationFunction(inState)

          #Check if it is a ghost, it it is a ghost, so don't come near it. Like min in minimax function
          if inHeight%numNowAgents != 0:
            #Make return value like infinity
            retValue = 1e6
            #Get list of legal action of state s
            #iterCount%numAgent to get agent indext 0->n
            listLegalAction = [x for x in inState.getLegalActions(inHeight%numNowAgents) if x != 'Stop']
            #Browser each of value in listLegalAction
            for action in listLegalAction:
              #Get all the successor and return the min all of it
              subState = inState.generateSuccessor(inHeight%numNowAgents,action)
              retValue = min(retValue, recursion(subState, inHeight+1))
            return retValue
          
          #Else it is pacman, so it is the max, return the max.
          else:
            #make result like -infinity
            retValue = -1e6
            listLegalAction = [x for x in inState.getLegalActions(inHeight%numNowAgents) if x != 'Stop']
            
            #Browser each of value in listLegalAction
            for a in listLegalAction:
              subState = inState.generateSuccessor(inHeight%numNowAgents,a)
              #Return the max of it.
              retValue = max(retValue, recursion(subState, inHeight+1))

              #It go to the top
              if inHeight == 0:
                ActionScore.append(retValue)

            return retValue
        
        #This is a temp to save the return value of this funcion. 
        #The thing we concern is the ActionScore, the max value of this list will be the result we want
        returnFuncValue = recursion(gameState, 0);

        return ([x for x in gameState.getLegalActions(0) if x != 'Stop'])[ActionScore.index(max(ActionScore))]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    #This is look like minimax agent. Add alpha and beta we have alphabeta agent. ^^
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #Data get from the MultiAgentSearchAgent class
        #Number of agent in the map
        numNowAgents = gameState.getNumAgents()
        ActionScore = []

        def recursion(inState, inHeight, alpha, beta):
          if inHeight >= self.depth*numNowAgents or inState.isWin() or inState.isLose():
            return self.evaluationFunction(inState)

          #Check if it is a ghost, it it is a ghost, so don't come near it. Like min in minimax function
          if inHeight%numNowAgents != 0:
            #Make return value like infinity
            retValue = 1e6
            #Get list of legal action of state s
            #iterCount%numAgent to get agent indext 0->n
            listLegalAction = [x for x in inState.getLegalActions(inHeight%numNowAgents) if x != 'Stop']
            #Browser each of value in listLegalAction
            
            for action in listLegalAction:
              #Get all the successor and return the min all of it
              subState = inState.generateSuccessor(inHeight%numNowAgents,action)
              retValue = min(retValue, recursion(subState, inHeight+1, alpha, beta))
              #Check if it can be done now
              beta = min(beta, retValue)
              #If it true, we don't need to check any more
              
              if beta < alpha:
                break
            return retValue
          
          #Else it is pacman, so it is the max, return the max.
          else:
            #make result like -infinity
            retValue = -1e6
            listLegalAction = [x for x in inState.getLegalActions(inHeight%numNowAgents) if x != 'Stop']
            #Browser each of value in listLegalAction
            
            for a in listLegalAction:
              subState = inState.generateSuccessor(inHeight%numNowAgents,a)
              #Return the max of it.
              retValue = max(retValue, recursion(subState, inHeight+1, alpha, beta))
              alpha = max(alpha, retValue)

              #It go to the top
              if inHeight == 0:
                ActionScore.append(retValue)
              
              if beta < alpha:
                break

            return retValue
        
        #This is a temp to save the return value of this funcion. 
        #The thing we concern is the ActionScore, the max value of this list will be the result we want
        #alpha: MAX's best option on path to root. Init it to -infinity
        #beta: MIN's best option on path to root. Init it to infinity

        returnFuncValue = recursion(gameState, 0, -1e6, 1e6);

        return ([x for x in gameState.getLegalActions(0) if x != 'Stop'])[ActionScore.index(max(ActionScore))]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    #A little like minimax but we don't use min, expectimax instead 
    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
                #Data get from the MultiAgentSearchAgent class
        #Number of agent in the map
        numNowAgents = gameState.getNumAgents()
        ActionScore = []


        def recursion(inState, inHeight):
          if inHeight >= self.depth*numNowAgents or inState.isWin() or inState.isLose():
            return self.evaluationFunction(inState)

          #Check if it is a ghost, it it is a ghost, so don't come near it. Like min in minimax function
          if inHeight%numNowAgents != 0:
            #Get the list of successor score to calculate the average value
            successorScore = []
            #Get list of legal action of state s
            #iterCount%numAgent to get agent indext 0->n
            listLegalAction = [x for x in inState.getLegalActions(inHeight%numNowAgents) if x != 'Stop']
            #Browser each of value in listLegalAction
            for action in listLegalAction:
              #Get all the successor and return the min all of it
              subState = inState.generateSuccessor(inHeight%numNowAgents,action)
              retValue = recursion(subState, inHeight+1)
              successorScore.append(retValue)

            #This save the average score in the expecimax        
            averageScore = 0        
            for i in range(len(successorScore)):
              averageScore = averageScore + successorScore[i]
              #Calculate the average. Not like abound, return min value
            averageScore = float(averageScore)/len(successorScore)

            return averageScore          

          #Else it is pacman, so it is the max, return the max.
          else:
            #make result like -infinity
            retValue = -1e6
            listLegalAction = [x for x in inState.getLegalActions(inHeight%numNowAgents) if x != 'Stop']
            
            #Browser each of value in listLegalAction
            for a in listLegalAction:
              subState = inState.generateSuccessor(inHeight%numNowAgents,a)
              #Return the max of it.
              retValue = max(retValue, recursion(subState, inHeight+1))

              #It go to the top
              if inHeight == 0:
                ActionScore.append(retValue)

            return retValue
        
        #This is a temp to save the return value of this funcion. 
        #The thing we concern is the ActionScore, the max value of this list will be the result we want
        returnFuncValue = recursion(gameState, 0);

        return ([x for x in gameState.getLegalActions(0) if x != 'Stop'])[ActionScore.index(max(ActionScore))]


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).
      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    #Some normal variable can be used
    pacmanPos = currentGameState.getPacmanPosition()
    foodPos = currentGameState.getFood().asList()
    allCapsules = currentGameState.getCapsules()
    ghostPos = currentGameState.getGhostStates()

    #We will valuate the score base on:    
    # + Score when eat food
    eatFoodScore = 0
    # + score when eat capsule
    eatCapsuleScore = 0
    # + Score when eat scared ghost
    eatScaredGhostScore = 0

    #This for calculate the score when eat food
    #It save all the distance from current pacman position to each food
    foodDist = []
    for food in foodPos:
      #1.0/ because we want to get the nearest, and value of each is one point.
      foodDist.append(1.0/manhattanDistance(pacmanPos, food))
    #Get the biggest score can reach
    if len(foodDist) > 0:
      eatFoodScore = max(foodDist)

    #This for calculate the score when eat capsule
    #This save all the distance from current pacman position to each capsule
    capsuleDist = []
    for capsule in allCapsules:
      #10.0 / because we want to get the nearst, and I think each capsule have the value
      #more than normal food.
      capsuleDist.append(10.0/manhattanDistance(pacmanPos, capsule))
    #Get the biggest score can reach
    if len(capsuleDist) > 0:
      eatCapsuleScore = max(capsuleDist)

    #This for calculate the score when eat scared ghost
    for ghost in ghostPos:
      disGhost = manhattanDistance(pacmanPos, ghost.getPosition())
      if ghost.scaredTimer > 0:
        eatScaredGhostScore += pow(max(8 - disGhost,0),2)
      else:
        eatScaredGhostScore -= pow(max(8 - disGhost,0),2)

    return currentGameState.getScore() + eatCapsuleScore + eatFoodScore + eatScaredGhostScore

# Abbreviation
better = betterEvaluationFunction
