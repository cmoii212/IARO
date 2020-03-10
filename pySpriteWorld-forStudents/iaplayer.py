# -*- coding: utf-8 -*-

import numpy as np
import heapq as hpq

class Player():
    """
    Class Player
    """
    def __init__(self, initState, goalState, wallStates, maxRow, maxCol):
        self.initState = initState
        self.goalState = goalState
        self.wallStates = wallStates
        self.maxRow = maxRow
        self.maxCol = maxCol
        self.state = initState
        self.precState = []

    def nextMove(self):
        raise NotImplementedError("Please implement this method")

    def toString(self):
        return "Player"

class HumanPlayer(Player):
    """
    Class Player Humain
    il attend une entrée pour choisir son prochain coup
    """
    
    def nextMove(self):
        
