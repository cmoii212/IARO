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
        # FRONTIERE NON VIDE ET OBJECTIF NON ATTEINT
        while frontiere != [] and goal != bestNode.state:
            # SELECTIONNE LE PLUS PETIT G DE LA FRONTIERE
            (min_f, bestNode) = hp.heappop(frontiere)
            # NOEUD JAMAIS EXPLORE
            if not(bestNode in reserve):
                reserve[bestNode] = bestNode.g
                # EXPLORE LES NOEUDS VOISINS
                nodes = bestNode.expand(problem)
                for node in nodes:
                    f = node.g + manhattan(node.state, goal)
                    # AJOUTE FRONTIERE NOEUD VOISINS
                    hp.heappush(frontiere, (f, node))
        # RETOURNE LE CHEMIN VERS SE NOEUD
        return bestNode.path()

class Problem():
    def __init__(self, shape, constraint):
        self.shape = shape
        self.dim = len(shape)
        self.mat = np.ones(shape, dtype=int)
        for c in constraint:
            self.mat[c] = 0
        self.inc = np.vstack((np.identity(self.dim, dtype=int), np.where(np.identity(self.dim, dtype =int) == 1, -1, 0)))
        
    def isAccessible(self, state):
        return self.isIn(state) and self.mat[state] == 1

    def successor(self, state):
        """tuple[int] -> List[tuple[int]]
        """
        neighboor = [tuple(np.asarray(state) + i) for i in self.inc if self.isIn(tuple(np.asarray(state) + i))]
        return [s for s in neighboor if self.isAccessible(s)]
        
    def isIn(self, state):
        try:
            self.mat[state]
            return True
        except IndexError:
            return False
        
    def isConstraint(self, state):
        return self.mat[state] == 0

    def immatriculation(self,state):
        res = state[0] * self.shape[1] + state[1]
        for i in range(1, self.dim - 1):
            res = self.shape[i+1] * res + state[i+1]
        return res
    
    def setAccessibility(self, state, accessible):
        """ tuple[int*] * boolean -> void
        """
        self.mat[state] = 1 if accessible else 0
    
class Board(Problem):
    def __init__(self, initStates, goalStates, wallStates, maxRow, maxCol):
        super().__init__((maxRow, maxCol), wallStates)
        self.playerStates = initStates
        self.goalStates = goalStates
        for state in self.playerStates:
            self.setAccessibility(state, False)
        
    def isGoalState(self, state):
        return state in self.goalStates

    def setGoalStates(self, goalStates):
        self.goalStates = goalStates
        
    def pickup(self, pos):
        self.goalStates.remove(pos)

    def setState(self, player, state):
        self.setAccessibility(self.playerStates[player], True)
        self.setAccessibility(state, False)
        self.playerStates[player] = state
        
    def goal(self, player):
        return self.goalStates[player]
    
    def show(self):
        tab = [["_" if self.isAccessible((i,j)) else "#" for i in range(self.shape[0])] for j in range(self.shape[1])]
        for r,c in self.playerStates:
            tab[r][c] = 'j'
        for r,c in self.goalStates:
            tab[r][c] = 'g'
        for i in range(len(tab)):
            tab[i] = ' '.join(tab[i])
        print('\n'.join(tab))

class timeBoard(Problem):
    def __init__(selfinitStates, goalStates, wallStates, maxRow, maxCol):
        # PLATEAU
        super().__init__((maxRow, maxCol), wallStates)
        # JOUEUR ET MURS
        self.playerStates = initStates
        self.goalStates = goalStates
        for state in self.playerStates:
            self.setAccessibility(state, False)
        # TEMPS
        self.currentTime = 0
        self.timeTable = dict() # Dict[(row,col,time)]:{0,1}
        
    def isAccessible(self, state):
        r,c,t = state
        return self.timeTable.get(state, super().isAccessible((r,c))) == 1

    def successor(self, state):
        """tuple[int] -> List[tuple[int]]
        """
        r,c,t = state
        state2D = (r,c)
        neighboor = [tuple(np.asarray(state2D) + i) for i in self.inc if self.isIn(tuple(np.asarray(state2D) + i))]
        return [(r,c,t+1) for r,c in neighboor if self.isAccessible((r,c,t+1))]
    
    def isConstraint(self, state):
        r,c,t = state
        return self.mat[(r,c)] == 0

    def isGoalState(self, state):
        return state in self.goalStates

    def setGoalStates(self, goalStates):
        self.goalStates = goalStates
        
    def pickup(self, pos):
        self.goalStates.remove(pos)

    def setState(self, player, state):
        self.setAccessibility(self.playerStates[player], True)
        self.setAccessibility(state, False)
        self.playerStates[player] = state
        
    def goal(self, player):
        return self.goalStates[player]
    
    def show(self):
        tab = [["_" if self.isAccessible((i,j)) else "#" for i in range(self.shape[0])] for j in range(self.shape[1])]
        for r,c in self.playerStates:
            tab[r][c] = 'j'
        for r,c in self.goalStates:
            tab[r][c] = 'g'
        for i in range(len(tab)):
            tab[i] = ' '.join(tab[i])
        print('\n'.join(tab))

    def tick(self):
        self.currentTime += 1
        
def manhattan(pos1, pos2):
    return abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1])

class Node():
    number = 0
    def __init__(self, state, parent=None):
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
    
    def expand(self, problem):
        if self.successor == []:
            self.successor = [Node(s, self) for s in problem.successor(self.state)]
        return self.successor
    
    def path(self):
        node, res = self, [self.state]
        while node.parent != None:
            res.insert(0,node.parent.state)
            node = node.parent
        return res
