from util import manhattanDistance
from game import Directions
import random, util
import math
from game import Agent
"""
Name - Janvi Sharma
UID: 3035552894
"""
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
       # print("score of all moves ", scores)
       # print("best score is ",bestScore)
        bestIndices = [index for index in range(len(scores)) if scores[index] >= bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
       # print("best indices are ", bestIndices)

        "Add more of your code here if you want to"
       # if chosenIndex:
       #   print("chosen")
       # else:
        #  print('no move')
        
       # print("move pac ",legalMoves[chosenIndex])
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
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [(ghostState.scaredTimer,ghostState.getPosition()) for ghostState in newGhostStates]
        powerP = currentGameState.getCapsules()

        evalue=0.0

        for x in newScaredTimes:
          dist = abs(newPos[0] - x[1][0]) + abs(newPos[1] - x[1][1])
          if(dist<2):
            # if we are close to the ghost 
            # we check if the ghost is scared of us or not
            if x[0]!=0:
              # ghost is scared of us
              # so we can explore more states without fear of dying
              evalue = evalue + 50
            else:
              # ghost can kill us
              # so we steer clear of ghost
              evalue = evalue - 5

        food_coordinates = prevFood.asList()
        for food in food_coordinates:
          dist = abs(food[0] - newPos[0]) + abs(food[1] - newPos[1])
          if dist == 0:
            # if we can eat the food at next position
            # give positive reward
            evalue = evalue + 15
          else:
            # else food reward is in reciprocal 
            # because farther the food, less rewarding it is to 
            # current state
            evalue = evalue + 1/dist
        
        for powerPellet in powerP:
          dist = abs(powerPellet[0] - newPos[0]) + abs(powerPellet[1] - newPos[1])
          if dist == 0:
            # if power pellet can be eaten
            # give massive positive reward 
            evalue = evalue + 25
          else:
            # same logic as food distance followed here as well
            evalue = evalue + 1/dist

        return evalue 
                
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
      def minUtil(gameState, agentIndex, depth):
        if gameState.isWin() or gameState.isLose():
          return gameState.getScore()
        else:
          legalActions = gameState.getLegalActions(agentIndex)
          if agentIndex + 1 != gameState.getNumAgents():
            nextPlayer = agentIndex + 1
          else:
            nextPlayer = 0 # pacman 
          
          if nextPlayer != 0:
            scores = [minUtil(gameState.generateSuccessor(agentIndex, action), nextPlayer, depth) for action in legalActions]
          else:
            if depth + 1 != self.depth:
              scores = [maxUtil(gameState.generateSuccessor(agentIndex, action), depth + 1) for action in legalActions]
            else:
              scores = [self.evaluationFunction(gameState.generateSuccessor(agentIndex, action)) for action in legalActions]
          return min(scores)
      
      def maxUtil(gameState, depth):
        if gameState.isWin() or gameState.isLose():
          # terminal states
          return gameState.getScore()
        else:
          legalActions = gameState.getLegalActions(0)
          scores = [minUtil(gameState.generateSuccessor(0,action), 1, depth) for action in legalActions]
          bestScore = max(scores)
          bestIndices = [index for index in range(len(scores)) if scores[index] >= bestScore]
          if depth!=0:
            return bestScore
          return bestIndices, legalActions

      bestIndices,legalActions = maxUtil(gameState, 0)
      chosenIndex = random.choice(bestIndices)
      return legalActions[chosenIndex]

    
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
      def minUtil(gameState, alpha, beta, depth, agentIndex):
        if gameState.isWin() or gameState.isLose():
          return gameState.getScore()
        else:
          if agentIndex + 1 != gameState.getNumAgents():
            nextPlayer = agentIndex + 1
          else:
            nextPlayer = 0 # pacman 

          legalActions = gameState.getLegalActions(agentIndex)
          minScore = float("inf")
          
          for x in legalActions:
            if nextPlayer != 0:
              currScore = minUtil(gameState.generateSuccessor(agentIndex, x), alpha, beta, depth, nextPlayer)
            elif depth + 1 != self.depth:
              currScore = maxUtil(gameState.generateSuccessor(agentIndex, x), alpha, beta, depth + 1)
            else:
              currScore = self.evaluationFunction(gameState.generateSuccessor(agentIndex, x))
            
            if currScore < minScore:
              minScore = currScore
            
            beta = min(beta, minScore)
            
            if minScore < alpha:
              return minScore
              
          return minScore
      def maxUtil(gameState, alpha, beta, depth):
        if gameState.isWin() or gameState.isLose():
          return gameState.getScore()
        else:
          maxScore = float("-inf")
          legalActions = gameState.getLegalActions(0)
          scores = []
          for x in legalActions:
            currScore = minUtil(gameState.generateSuccessor(0, x), alpha, beta, depth, 1)
            scores.append(currScore)
            
            if currScore > maxScore:
              # keep track of maximum score 
              maxScore = currScore

            alpha = max(alpha, maxScore)
            if maxScore > beta:
              return maxScore

          if depth!=0:
            return maxScore
          bestIndices = [index for index in range(len(scores)) if scores[index] >= maxScore]
          return bestIndices, legalActions
      
      bestIndices,legalActions = maxUtil(gameState, float("-inf"), float("inf"), 0)
      chosenIndex = random.choice(bestIndices)
      return legalActions[chosenIndex]        

class ExpectimaxAgent(MultiAgentSearchAgent):
  def getAction(self, gameState):
    def minUtil(gameState, agentIndex, depth):
      if gameState.isWin() or gameState.isLose():
        return gameState.getScore()
      else:
        legalActions = gameState.getLegalActions(agentIndex)
        if agentIndex + 1 != gameState.getNumAgents():
          nextPlayer = agentIndex + 1
        else:
          nextPlayer = 0 # pacman 
    
        if nextPlayer != 0:
          scores = [minUtil(gameState.generateSuccessor(agentIndex, action), nextPlayer, depth) for action in legalActions]
        else:
          if depth + 1 != self.depth:
            scores = [maxUtil(gameState.generateSuccessor(agentIndex, action), depth + 1) for action in legalActions]
          else:
            scores = [self.evaluationFunction(gameState.generateSuccessor(agentIndex, action)) for action in legalActions]
        expectancy = 0 
        norm = 1/len(legalActions)
        for x in scores: 
          expectancy += x*norm
        return expectancy

    def maxUtil(gameState, depth):
      if gameState.isWin() or gameState.isLose():
        # terminal states
        return gameState.getScore()
      else:
        legalActions = gameState.getLegalActions(0)
        scores = [minUtil(gameState.generateSuccessor(0,action), 1, depth) for action in legalActions]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] >= bestScore]
        if depth!=0:
          return bestScore
        return bestIndices, legalActions

    bestIndices,legalActions = maxUtil(gameState, 0)
    chosenIndex = random.choice(bestIndices)
    return legalActions[chosenIndex]

      
def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).
  """
  """
    Factors to consider:
    (1) Total number of food available
    (2) Total number of power pellets available -> need to test this more, current factoring gives randomized results, 
                                                  so left out from implementation
    (3) Distance from ghosts
    (4) Any close by food? Any close by pellets? Any close by ghosts?
    (5) Sum of all distances of food pellets 
  
  We would like pacman to ideally consider various factors when choosing a state as its successor.
  So to evaluate the goodness of a state we consider:
    -> sum of distances of food pellets, if this is large, penalize this state
    -> if we eat a power pellet at this state, then give large reward
    -> if power pellet is close, give positive reward 
    -> if pacman is suitably far from the ghost and close to a food pellet, then give positive reward 
    -> also, if the number of food pellets remaining is less, give positive reward, because
      we want to force pacman to eat all the food pellets
  """
  powerPellets = currentGameState.getCapsules()
  food_coordinates = currentGameState.getFood().asList()
  ghostStates = currentGameState.getGhostStates()
  pos = currentGameState.getPacmanPosition()
  scaredTimes = [(ghostState.scaredTimer,ghostState.getPosition()) for ghostState in ghostStates]

  evalue = 0.0
  evalue = currentGameState.getScore() 

  min_food_dist = float('inf')
  total_food_distance = 0 
  for x in food_coordinates:
    dist = util.manhattanDistance(x, pos)
    total_food_distance += dist 
    if dist < min_food_dist:
      min_food_dist = dist 
  if len(food_coordinates) == 0:
    min_food_dist = 1
  evalue = evalue - (2 * total_food_distance)/5

  min_ghost_dist = float('inf')
  for x in scaredTimes:
    dist = util.manhattanDistance(x[1], pos)
    if dist < min_ghost_dist:
      min_ghost_dist = dist 
  
  for x in powerPellets:
    dist = util.manhattanDistance(x, pos)
    if dist == 0:
      evalue += 2
    else:
      evalue += 1/(dist**2)
  
  if min_food_dist < min_ghost_dist + 2.7:
    evalue = evalue * 1.8
  
  evalue += 3/(len(food_coordinates)**2) if len(food_coordinates)!=0 else evalue 
  return evalue

# Abbreviation
better = betterEvaluationFunction

