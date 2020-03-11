# -*- coding: utf-8 -*-
import random as rd
import numpy as np
import heapq as hp

inc = [(0,1),(0,-1),(1,0),(-1,0)]

def movePlayer(joueur, player, state):
    player.set_rowcol(state[0], state[1])
    joueur.setState(state)

def playerPickup(game, joueur, player):
    joueur.pickup()
    o = player.ramasse(game.layers)
    return o

def AStar(state, goal, problem):
        nodeInit = Node(state)
        frontiere = [(nodeInit.g + manhattan(state, goal), nodeInit)]
        reserve = {}
        bestNode = nodeInit
        while frontiere != [] and goal != bestNode.state:
            #c = input()
            #print(frontiere)
            #print(reserve)
            (min_f, bestNode) = hp.heappop(frontiere)
            #print((min_f, bestNode))
            if not(problem.immatriculation(bestNode.state) in reserve):
                reserve[problem.immatriculation(bestNode.state)] = bestNode.g
                nodes = bestNode.expand(problem)
                #print('\t',nodes)
                for node in nodes:
                    f = node.g + manhattan(node.state, goal)
                    hp.heappush(frontiere, (f, node))
        #print(frontiere)
        #print(reserve)
        return bestNode.path()

class Problem():
    def __init__(self, shape, constraint):
        self.shape = shape
        self.constraint = constraint
        self.dim = len(shape)
        
    def isIn(self, state):
        for i in range(self.dim):
            if not(0 <= state[i] <= self.shape[i]):
                return False
        return not self.isConstraint(state)
    
    def isConstraint(self, state):
        return state in self.constraint

    def immatriculation(self,state):
        res = state[0] * self.shape[1] + state[1]
        for i in range(1, self.dim - 1):
            res = self.shape[i+1] * res + state[i+1]
        return res
    
class Board(Problem):
    def __init__(self, initStates, goalStates, wallStates, maxRow, maxCol):
        super().__init__((maxRow, maxCol), wallStates)
        self.playerStates = initStates
        self.goalStates = goalStates

    def isGoalState(self, state):
        return state in self.goalStates

    def setGoalStates(self, goalStates):
        self.goalStates = goalStates
        
    def pickup(self, pos):
        self.goalStates.remove(pos)

    def setState(self, player, state):
        self.playerStates[player] = state

    def goal(self, player):
        return self.goalStates[player]

    def isAccessible(self, state):
        return self.isIn(state) and not(state in self.playerStates)
    
    def show(self):
        tab = [["_" for i in range(self.shape[0])] for j in range(self.shape[1])]
        for r,c in self.playerStates:
            tab[r][c] = 'j'
        for r,c in self.goalStates:
            tab[r][c] = 'g'
        for r,c in self.constraint:
            tab[r][c] = '#'
        for i in range(len(tab)):
            tab[i] = ' '.join(tab[i])
        print('\n'.join(tab))

def manhattan(pos1, pos2):
    return abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1])

class Node():
    number = 0
    def __init__(self, state,parent=None):
        self.state = state
        self.parent = parent
        self.successor = []
        self.g = 0 if parent == None else parent.g + 1
        self.id = Node.number
        Node.number += 1
    def __eq__(self, other):
        """
        other -> boolean Or NotImplemented
        Retourne True si les noeud contienne le meme etat, sinon False
        """
        if isinstance(other, Node):
            return self.state == other.state
        return False
    def __lt__(self, other):
        """
        other -> boolean Or NotImplemented
        retourne True si le coût du noeud actuelle est inférieur au noeud 
        spécifié.
        """
        if isinstance(other, self.__class__):
            return self.g < other.g
        return NotImplemented
    def __hash__(self):
        return hash(self.state)
    def __repr__(self):
        return 'Node(%d,%d)'%(self.state[0], self.state[1])
    def __str__(self):
        return 'Node(%d,%d)'%(self.state[0], self.state[1])
    def expand(self, board):
        if self.successor == []:
            r, c = self.state
            self.successor = [Node((r+i,c+j), self) for (i,j) in inc if board.isAccessible((r+i, c+j))]
        return self.successor
    def path(self):
        node, res = self, [self.state]
        while node.parent != None:
            res.insert(0,node.parent.state)
            node = node.parent
        return res
