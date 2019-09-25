"""


"""





import time
import functools

bwins = 0
smts = 0
tcount = 0
wwins = 0
initial = time.time()


for i in range(0,1000):

    t0 = time.time()
    test = Chessgame(False)
    test.Testing = False
    test.pseudoAI = 'yes'
    turn,winner = test()
    elapsed = time.time() - t0
    total = time.time()-initial
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