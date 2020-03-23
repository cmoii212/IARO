# -*- coding: utf-8 -*-
from utils import *

inc = [(0,1),(0,-1),(1,0),(-1,0)]
inputs = {'w':(-1,0), 'z':(-1,0), 'up':(-1,0)
          , 'left':(0,-1), 'a':(0,-1), 'q':(0,-1)
          , 's':(1,0), 'down':(1,0)
          , 'd':(0,1), 'right':(0,1)}
pattern = "\tw\n\t^\n\t|\n  a < --.-- > d\n\t|\n\tˇ\n\ts"

class Player():
    """
    Class Player
    """
    number = 0
    def __init__(self, initState, index, board):
        self.state = initState
        self.board = board
        self.index = index
        self.precState = []
        self.id = Player.number + 1
        Player.number += 1
        
    def nextMove(self):
        raise NotImplementedError("Please implement this method")

    def toString(self):
        return "Player %0d"%self.id

    def isAccessible(self,state):
        """
        Retourne le boolean indiquant si la position est accessible par le joueur
        """
        return self.board.isAccessible(state)

    def isGoalState(self, pos):
        return self.board.isGoalState(pos)

    def pickup(self):
        self.board.pickup(self.state)
    
    def setState(self, state):
        self.precState.append(self.state)
        self.state = state
        self.board.setState(self.index, state)

def human_player_input():
    choice = input("direction :")
    if choice in inputs.keys():
        return inputs[choice]
    return 0,0

class HumanPlayer(Player):
    """
    Class Player Humain
    il attend une entrée pour choisir son prochain coup
    """
    
    def nextMove(self):
        r, c = self.state
        nextStates = board.successor(self.state)
        print(nextStates)
        print(pattern)
        nextState = None
        while not nextState:
            nr, nc = human_player_input()
            nextState = None if nr == nc == 0 else (r + nr, c + nc)
            if nextState != None:
                nextState = nextState if self.isAccessible(nextState) else None
        return nextState
    
    def toString(self):
        return "Human Player %0d"%self.id

class RandomPlayer(Player):
    """
    Class Player Humain
    il attend une entrée pour choisir son prochain coup
    """
    
    def nextMove(self):
        r, c = self.state
        nextStates = board.successor(self.state)
        return rd.choice(nextStates)
    
    def toString(self):
        return "Random Player %0d"%self.id

class AStarPlayer(Player):
    """
    A* pathfinding agent with local repair
    """
    def __init__(self, initState, index, board):
        super().__init__(initState, index, board)
        self.path = []
        self.step = -1

    def updatePath(self):
        self.path = AStar(self.state, self.board.goal(self.index), self.board)
        self.step = 1 if len(self.path) > 1 else 0

    def process(self):
        if self.path == []:
            self.updatePath()
        else:
            # Le chemin ne mene plus a l'objectif
            if self.path[-1] != self.board.goal(self.index):
                self.updatePath()
            #Si le chemin est bloqué
            elif not self.board.isAccessible(self.path[self.step]):
                self.updatePath()
            #Continue le chemin calcule
            else:
                self.step += 1
            
    def nextMove(self):
        self.process()
        return self.path[self.step]
            
    
    def toString(self):
        return "A* Player %0d"%self.id

class CoopAstar(Player):
    """
    A* pathfinding agent with local repair
    """
    def __init__(self, initState, index, timeBoard):
        super().__init__(initState, index, timeBoard)
        self.path = []
        self.step = -1
        
    def process(self):
        return 0
    
    def nextMove(self):
        self.process()
        return self.initState

    def toString(self):
        return "Coop A* Player %0d"%self.id
