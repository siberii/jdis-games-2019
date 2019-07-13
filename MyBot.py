# MyBot.py
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

import random
import time
from pacman.game import Directions
import pacman.util as util  # Free utility functions like Stack or Queue !
from typing import Tuple, List
from pacman.capture import GameState
from pacman.captureAgents import CaptureAgent


def getMostProbableManhattanDistance(yourPosition: Tuple[int, int], ennemyIndex: int, gamestate: GameState) -> List[int]:
    agentDistance = gamestate.getAgentDistances()[ennemyIndex]
    proba = 0.0
    distances = []
    bounce = 0
    while proba < 0.75:
        currentDistance = agentDistance+bounce
        proba += gamestate.getDistanceProb(currentDistance, agentDistance)
        if (currentDistance not in distances):
            distances.append(currentDistance)
        currentDistance = agentDistance-bounce
        proba += gamestate.getDistanceProb(currentDistance, agentDistance)
        if (currentDistance not in distances):
            distances.append(currentDistance)
        bounce += 1
    return distances


def isProbablyCloserThan(yourPosition: Tuple[int, int], ennemyIndex: int, gamestate: GameState, worryDistance: int):
    probableDistances = getMostProbableManhattanDistance(yourPosition, ennemyIndex, gamestate)
    for distance in probableDistances:
        if worryDistance > distance:
            return True
    return False


def isAlreadyBetter(cell, dict, currentCount):
    if cell in dict:
        if(dict[cell] <= currentCount):
            return True
        else:
            return False
    else:
        return False


def isInList(myList, point) -> bool:
    for element in myList:
        if element[0] == point:
            return True
    return False


def getAdjacent(tile: Tuple[int, int]) -> List[Tuple[int, int]]:
    x = tile[0]
    y = tile[1]
    listOfAdjacent = []
    listOfAdjacent.append((x+1, y))
    listOfAdjacent.append((x, y+1))
    listOfAdjacent.append((x-1, y))

    listOfAdjacent.append((x, y-1))
    return listOfAdjacent


def findDirection(dict, origin: Tuple[int, int]) -> str:
    closest = 1000
    direction = Directions.NORTH
    west = (origin[0]+1, origin[1])
    east = (origin[0]-1, origin[1])
    south = (origin[0], origin[1]+1)
    north = (origin[0], origin[1]-1)

    if (west in dict and dict[west] < closest):
        closest = dict[west]
        direction = Directions.EAST
    if (east in dict and dict[east] < closest):
        closest = dict[east]
        direction = Directions.WEST
    if (south in dict and dict[south] < closest):
        closest = dict[south]
        direction = Directions.NORTH
    if (north in dict and dict[north] < closest):
        closest = dict[north]
        direction = Directions.SOUTH
    return direction


def AddToQueue(actualTile: Tuple, toCheck: List, dict, grid):
    adjacentCells = getAdjacent(actualTile)
    for cell in adjacentCells:
        if(not grid[cell[0]][cell[1]]
           and not isAlreadyBetter(cell, dict, dict[actualTile]+1)):
            dict[cell] = dict[actualTile]+1
            toCheck.append(cell)


def getDirectionAndDistance(fromPoint: Tuple[int, int], toPoint: Tuple[int, int], gamestate: GameState) -> Tuple[int, str]:
    grid = gamestate.getWalls()

    myDict = {(toPoint[0], toPoint[1]): 0}
    toCheck = [(toPoint[0], toPoint[1])]
    distance = 0
    while fromPoint not in myDict:
        AddToQueue(toCheck[distance], toCheck, myDict, grid)
        distance += 1
    isInList(myDict, fromPoint)

    return (distance, findDirection(myDict, fromPoint))


#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed):
    """
    This function should return a list of two agents that will form the
    team, initialized using firstIndex and secondIndex as their agent
    index numbers. isRed is True if the red team is being created, and
    will be False if the blue team is being created.
    """

    # The following line is an example only; feel free to change it.
    return [AgentOne(firstIndex), AgentTwo(secondIndex)]

##########
# Agents #
##########


class AgentOne(CaptureAgent):
    gridWall = []
    mapMiddlePoint = []

    """
    A Dummy agent to serve as an example of the necessary agent structure.
    You should look at baselineTeam.py for more details about how to
    create an agent as this is the bare minimum.
    """

    def registerInitialState(self, gameState: GameState):
        """
        This method handles the initial setup of the
        agent to populate useful fields (such as what team
        we're on).

        A distanceCalculator instance caches the maze distances
        between each pair of positions, so your agents can use:
        self.distancer.getDistance(p1, p2)

        IMPORTANT: This method may run for at most 5 seconds.
        """

        '''
        Make sure you do not delete the following line. If you would like to
        use Manhattan distances instead of maze distances in order to save
        on initialization time, please take a look at
        CaptureAgent.registerInitialState in captureAgents.py.
        '''
        CaptureAgent.registerInitialState(self, gameState)

        '''
        Your initialization code goes here, if you need any.
        '''
        self.minFoodxy = (0, 0)

        self.gridWall = gameState.getWalls()

        if (self.index in gameState.getRedTeamIndices()):
            # left side
            self.mapMiddlePoint = (self.gridWall.width//2 - 2, self.gridWall.height//2)
            self.foodInMouth = 0
        else:
            # right side
            self.mapMiddlePoint = (self.gridWall.width//2 + 2, self.gridWall.height//2)
            self.foodInMouth = 0

    def chooseAction(self, gameState: GameState) -> str:
        """
        Picks among legal actions randomly.
        """
        ownIndex = self.index
        ownPosition = gameState.getAgentPosition(ownIndex)

        if (ownIndex in gameState.getBlueTeamIndices()):
            if self.foodInMouth < 2 and self.findNbFoodLeft(gameState.getRedFood(), gameState) > 0:
                direction = self.findClosestFoodDirection(gameState.getRedFood(), gameState)
                print("goFood")
            else:
                direction = getDirectionAndDistance(ownPosition, self.mapMiddlePoint, gameState)[1]
                print("goHome")
                if ownPosition == self.mapMiddlePoint:
                    self.foodInMouth = 0
            print(self.foodInMouth)

        else:
            if self.foodInMouth < 2 and self.findNbFoodLeft(gameState.getRedFood(), gameState) > 0:
                direction = self.findClosestFoodDirection(gameState.getBlueFood(), gameState)
            else:
                direction = getDirectionAndDistance(ownPosition, self.mapMiddlePoint, gameState)[1]
                if ownPosition == self.mapMiddlePoint:
                    self.foodInMouth = 0

        return direction

    def findClosestFoodDirection(self, grid, gameState: GameState) -> str:
        if (self.index in gameState.getBlueTeamIndices()):
            if (self.minFoodxy == gameState.getAgentPosition(self.index)):
                self.foodInMouth += 1
            print(self.minFoodxy, gameState.getAgentPosition(self.index))

        minFood = -1
        minFoodxy = (0, 0)
        ownPosition = gameState.getAgentPosition(self.index)
        for i in range(grid.width):
            for j in range(grid.height):
                if grid[i][j]:
                    if minFood == -1:
                        minFood = getDirectionAndDistance(ownPosition, (i, j), gameState)
                        minFoodxy = (i, j)
                    elif minFood[0] > getDirectionAndDistance(ownPosition, (i, j), gameState)[0]:
                        minFood = getDirectionAndDistance(ownPosition, (i, j), gameState)
                        minFoodxy = (i, j)

        self.minFoodxy = minFoodxy
        if type(minFood) is int:
            return Directions.NORTH
        return minFood[1]

    def findNbFoodLeft(self, grid, gameState: GameState) -> int:
        nBFood = 0
        for i in range(grid.width):
            for j in range(grid.height):
                if grid[i][j]:
                    nBFood += 1
        return nBFood


Behavior = {
    'PULL': 'PULL',
    'PUSH': 'PUSH',
    'PATROL': 'PATROL',
    'FOLLOW': 'FOLLOW'
}


class AgentTwo(CaptureAgent):
    gridWall = []
    mapMiddlePoint = []
    currBehavior = Behavior['PUSH']
    currDestination = []
    initialPosition = []
    currPosition = []

    def registerInitialState(self, gameState: GameState):
        CaptureAgent.registerInitialState(self, gameState)
        self.gridWall = gameState.getWalls()
        self.mapMiddlePoint = (self.gridWall.width//2, self.gridWall.height//2)
        self.initialPosition = gameState.getAgentPosition(self.index)
        self.currPosition = self.initialPosition

    def chooseAction(self, gameState: GameState) -> str:
        # Threat evaluation
        self.updatePosition(gameState)

        # update behavior according to threat evaluation
        if self.currPosition == self.mapMiddlePoint and self.currBehavior == Behavior['PUSH']:
            self.currBehavior = Behavior['PULL']
        else:
            self.currBehavior = Behavior['PUSH']

        # update action according to behavior
        if self.currBehavior == Behavior['PUSH']:
            self.currDestination = self.mapMiddlePoint
        elif self.currBehavior == Behavior['PULL']:
            self.currDestination = self.initialPosition

        return getDirectionAndDistance(gameState.getAgentPosition(self.index), self.currDestination, gameState)[1]

    def updatePosition(self, gameState):
        self.currPosition = gameState.getAgentPosition(self.index)
