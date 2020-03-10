# -*- coding: utf-8 -*-

inc = [(0,1),(0,-1),(1,0),(-1,0)]

def movePlayer(joueur, player, state):
    player.set_rowcol(state[0], state[1])
    joueur.setState(state)

def playerPickup(game, joueur):
    joueur.pickup()
    o = game.player.ramasse(game.layers)
    return o

class Board():
    def __init__(self, initStates, goalStates, wallStates, maxRow, maxCol):
        self.playerStates = initStates
        self.goalStates = goalStates
        self.wallStates = wallStates
        self.maxRow = maxRow
        self.maxCol = maxCol
        
    def isIn(self,pos):
        """
        Retourne le boolean indiquant si la position est accessible par le joueur
        """
        return pos not in self.wallStates and 0 <= pos[0] <= self.maxRow and 0 <= pos[1] <= self.maxCol
    
    def isWall(self,pos):
        return pos in self.wallStates

    def isGoalState(self, pos):
        return pos in self.goalStates

    def setGoalStates(self, goalStates):
        self.goalStates = goalStates

    def pickup(self, pos):
        self.goalStates.remove(pos)

    def setState(self, player, state):
        self.playerStates[player] = state

    def goal(self, player):
        return self.goalStates[player]
    def show(self):
        tab = [["_" for i in range(self.maxCol)] for j in range(self.maxRow)]
        for r,c in self.playerStates:
            tab[r][c] = 'j'
        for r,c in self.goalStates:
            tab[r][c] = 'g'
        for r,c in self.wallStates:
            tab[r][c] = '#'
        for i in range(len(tab)):
            tab[i] = ' '.join(tab[i])
        print('\n'.join(tab))

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
    def expand(self, board):
        if self.successor == []:
            r, c = self.state
            self.successor = [Node((r+i,c+j), self) for (i,j) in inc if board.isIn((r+i, c+j))]
        return self.successor
    def path(self):
        node, res = self, [self.state]
        while node.parent != None:
            res.insert(0,node.parent.state)
            node = node.parent
        return res
    def immatriculation(self, board):
        r, c = self.state
        return r * board.maxRow + c
