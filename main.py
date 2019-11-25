
from multiprocessing import freeze_support,Pool,set_start_method
import time
import functools
from ChessAI_semirandom import *
from ChessAI_alphabeta import  *
from ChessBoard import *


if __name__ == '__main__':

    # setting up multiprocessing conditions
    freeze_support()
    set_start_method('spawn')

    # initializing win counts
    bwins = 0 # Black AI Wins
    smts = 0 # Stalemate
    tcount = 0 # Max Turns Exceeded
    wwins = 0 # White AI Wins
    initial = time.time() # effectively t0 for starting this


    #Loops through n number of games while tracking and printing win counts
    for i in range(0,1000):

        t0 = time.time()
        game = Chessgame() # creates a new game
        game.Testing = False
        turn,winner = game(MultiprocessAB,RandomAI) # returns the round turn count and winner
        elapsed = time.time() - t0 # round time
        total = time.time()-initial # total process time
        if winner == 'Black':bwins += 1
        elif winner == 'White': wwins += 1
        elif winner == 'Stalemate': smts += 1
        else: tcount +=1
        if turn == 150:
            print('\nIteration: '+str(i)+'\nRun Time - '+'%0.4fs' % (elapsed)+'\nTotal Duration - '+'%0.4fs' % (total)+
                  '\nResult: '+winner+ '\nWhite Wins: '+str(wwins)+'\nBlack Wins: '+str(bwins)+
                  '\nStalemates: '+str(smts)+'\nInconclusive: '+str(tcount))
        else:
            print('\nIteration: ' +str(i)+'\nRun Time - '+'%0.4fs' % (elapsed)+'\nTotal Duration - '+'%0.4fs' % (total)
                  +'\nResult: Player ' + winner + ' Victory'+'\nTurns: '+str(turn)+
                  '\nWhite Wins: ' + str(wwins) + '\nBlack Wins: ' + str(bwins) + '\nStalemates: ' + str(smts)
                  + '\nInconclusive: ' + str(tcount))


