# -*- coding: utf-8 -*-

# Nicolas, 2015-11-18

from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
import pygame
import glo

import iaplayer as Joueur
from utils import *

import random 
import numpy as np
import sys


# ---- ---- ---- ---- ---- ----
# ---- Misc                ----
# ---- ---- ---- ---- ---- ----



# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    name = _boardname if _boardname is not None else 'pathfindingWorld3'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    player = game.player
    
def main():

    #for arg in sys.argv:
    iterations = 100 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()
    

    
    #-------------------------------
    # Building the matrix
    #-------------------------------
       
           
    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print ("Init states:", initStates)
    
    # on localise tous les objets ramassables
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)
        
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)

    #-------------------------------    
    # Initialisation du joueur
    #-------------------------------
    board = Board(initStates, goalStates, wallStates, 21, 21)
    joueur = Joueur.AStarPlayer(initStates[0], 0,board)
    
    #-------------------------------
    # Building the best path with A*
    #-------------------------------
    

    
    
        
    #-------------------------------
    # Moving along the path
    #-------------------------------
        
    # bon ici on fait juste un random walker pour exemple...
    

    row,col = initStates[0]
    #row2,col2 = (5,5)

    for i in range(iterations):
        next_row ,next_col = joueur.nextMove()
        if ((next_row,next_col) not in wallStates) and next_row>=0 and next_row<=20 and next_col>=0 and next_col<=20:
            movePlayer(joueur, player, (next_row,next_col))
            print ("pos 1:",next_row,next_col)
            game.mainiteration()
            row, col =  next_row ,next_col
        # si on a  trouvé l'objet on le ramasse
        if (row,col)==goalStates[0]:
            o = playerPickup(game, joueur, player)
            game.mainiteration()
            print ("Objet trouvé!", o)
            break
        '''
        #x,y = game.player.get_pos()
    
        '''
    pygame.quit()
    
        
    
   

if __name__ == '__main__':
    main()
    


