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
from pacman.game import Directions
import pacman.util as util # Free utility functions like Stack or Queue ! 
from typing import Tuple, List
from pacman.capture import GameState
from pacman.captureAgents import CaptureAgent


def isAlreadyBetter(cell,queue):
    for element in queue:
        if cell[0]==element[0]:
            if element[1]<cell[1]:
                return True
            else:
                return False 
    return False
    

def isInList(myList, point)->bool:
    for element in myList:
        if element[0]==point:
            return True
    return False

def getAdjacent(tile:Tuple[int,int])->List[Tuple[int,int]]:
    x=tile[0]
    y=tile[1]
    listOfAdjacent=[]
    listOfAdjacent.append((x+1,y))
    listOfAdjacent.append((x,y+1))
    listOfAdjacent.append((x-1,y))
    listOfAdjacent.append((x,y-1))
    return listOfAdjacent

def findDirection(queue:List,origin: Tuple[int,int])->str:
    reverseQueue= reversed(queue)
    adjacentCells=getAdjacent(origin)
    for element in reverseQueue:
        if element[0] in adjacentCells:
            if element[0][0]+1==origin[0]:
                return Directions.WEST
            elif element[0][0]-1==origin[0]:
                return Directions.EAST
            elif element[0][1]+1==origin[1]:
                return Directions.SOUTH
            else:
                return Directions.NORTH
    return





def AddToQueue(tile:Tuple, queue, grid):
    adjacentCells=getAdjacent(tile[0])
    goodCells=[]
    for cell in adjacentCells:
        if(not grid[cell[0]][cell[1]]
           and not isAlreadyBetter((cell,tile[1]+1),queue)):
           goodCells.append((cell,tile[1]+1))
    queue+=goodCells

    
def getDirectionAndDistance(fromPoint:Tuple[int,int],toPoint:Tuple[int,int], gamestate:GameState) -> Tuple[int,str]:
    grid =gamestate.getWalls()

    myList=[((toPoint[0],toPoint[1]),0)]

    index=0
    while (not isInList(myList,fromPoint)):
        AddToQueue(myList[index], myList, grid)
        index+=1
    return (index,findDirection(myList,fromPoint))


    

    

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
        self.gridWall = gameState.getWalls()
        self.mapMiddlePoint = (self.gridWall.width//2, self.gridWall.height//2)
        print(self.mapMiddlePoint)
        

    def chooseAction(self, gameState: GameState) -> str:
        """
        Picks among legal actions randomly.
        """
        ownIndex=self.index
        print(ownIndex)
        ownPosition=gameState.getAgentPosition(ownIndex)
        print(ownPosition)
        destination = self.mapMiddlePoint
        # if (ownIndex in gameState.getBlueTeamIndices()):
        #     destination=gameState.getRedFood()[0]
        # else:
        #     destination=gameState.getBlueFood()[0]

        direction=getDirectionAndDistance(ownPosition,destination,gameState)[1]
        print (direction)
        return direction



class AgentTwo(CaptureAgent):
    def registerInitialState(self, gameState: GameState):
        CaptureAgent.registerInitialState(self, gameState)
    
    def chooseAction(self, gameState: GameState) -> str:
        actions = gameState.getLegalActions(self.index)
        return random.choice(actions)
