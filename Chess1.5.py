"""


"""





import copy
import random as r
from collections import defaultdict

from colorama import Fore, Back, Style
import time
import functools

class Chessgame():
    Names = ['Rook', 'Knight', 'Bishop',
             'Queen', 'King', 'Pawn']
    opponent = {'Black': 'White', 'White': 'Black'}

    def __init__(self, isAI):
        self.isAI = isAI
        self.board = []
        self.board_state = []
        self.current = []
        self._current_state_raw = {}
        self.setup()
        self.is_in_check = False
        self.testvalue = None
        self.Testing = False
        self.testing_holdback=[]

    def setup(self):
        if self.isAI == False:
            self._setup()
            self.king_check = {'Black': [], 'White': []}
            self.turn_count = 0

    class Piece():
        ''' Each subclass of the piece object has it\'s own function for checking the movment range against the
    imputted move. Currently the way most of them work is by testing every appicable string combination for a given piece
    (i.e. a-z,5 or a,1-5 for a rook) and discarding the ones that are invalid

    '''
        def __init__(self, playerID):
            self.owner = playerID
            self.piece = 'Undef'
            self.value = 0
            self.avalible_moves = False
            self.kc_moves = {}

        def check_if_changed(self,current_board, is_king_check=False):
            if not self.avalible_moves:
                self.move_range(current_board,is_king_check)
                return [*self.avalible_moves.keys()]
            for move in self.avalible_moves.keys():
                if current_board[move] == self.avalible_moves[move]:
                    continue
                else:
                    self.move_range(current_board,is_king_check)
                    break

            return [*self.avalible_moves.keys()]

        def __str__(self):
            return self.piece + ' '  # self.owner + self.piece

        def getpos(self, current_state_raw):
            self.position = "".join([k for k, v in current_state_raw.items() if self == current_state_raw[k]])

        def move_range(self,current_state_raw,is_king_check = False):
            up_right, up_left, down_right, down_left, up, down, left, right = \
                self.position, self.position, self.position, self.position, self.position, self.position, self.position, self.position
            if self.piece == 'Twr':
                up_right,up_left,down_right,down_left = -1,-1,-1,-1
            elif self.piece == 'Bsp':
                up,down,left,right = -1,-1,-1,-1
            moves = []
            for i in range(1, 8):
                if up_left == up_right == down_left == down_right == up == down == left == right == -1:break
                up_right = (chr(ord(self.position[0]) + i) + str(int(self.position[1]) + i)) if up_right != -1 else -1
                up_left = (chr(ord(self.position[0]) - i) + str(int(self.position[1]) - i)) if up_left != -1 else -1
                down_right = (chr(ord(self.position[0]) + i) + str(int(self.position[1]) - i)) if down_right != -1 else -1
                down_left = (chr(ord(self.position[0]) - i) + str(int(self.position[1]) + i)) if down_left != -1 else -1
                up = (chr(ord(self.position[0]) + i) + str(int(self.position[1]))) if up != -1 else -1
                down = (chr(ord(self.position[0]) - i) + str(int(self.position[1]))) if down != -1 else -1
                left = (chr(ord(self.position[0])) + str(int(self.position[1]) - i)) if left != -1 else -1
                right = (chr(ord(self.position[0])) + str(int(self.position[1]) + i)) if right != -1 else -1
                next = [str(up_right), str(up_left), str(down_right),
                        str(down_left), str(up), str(down), str(left), str(right)]
                pots = [x for x in next if x[0] in 'abcdefgh' and x[1] in '12345678']
                if is_king_check:[x for x in pots]
                else: pots = [x for x in pots if (current_state_raw[x]).owner != self.owner]
                for x in pots:
                    if (current_state_raw[x]).owner == Chessgame.opponent[self.owner]:
                        if is_king_check:
                            if (current_state_raw[x]).piece == 'Kng':
                                moves.append(x)
                        else:
                            moves.append(x)
                            pots.remove(x)
                [moves.append(x) for x in pots]
                for x in next:
                    if is_king_check:
                        next[next.index(x)] = -1 if x not in pots else -1 \
                            if current_state_raw[x].owner == self.owner else x
                    else: next[next.index(x)] = -1 if x not in pots else x

                if self.piece != 'Kng':
                    up_right, up_left, down_right, down_left, up, down, left, right = next
                else:
                    up_right, up_left, down_right, down_left, up, down, left, right = -1,-1,-1,-1,-1,-1,-1,-1
            if is_king_check:
                return moves
            else :
                self.avalible_moves = {move:current_state_raw[move] for move in moves} if moves else {}


    class Dummy(Piece):

        """
        This is the object used in blank spaces, given that it doesn't really take up any memory it's worth it for
        the convenience alone
        """

        def __init__(self):
            self.owner = 'None'
            self.piece = "Not a Piece"
            self.value = 0
        def __str__(self):
            return ' '

    class Pawn(Piece):
        def __init__(self, playerID):
            super().__init__(playerID)
            self.piece = 'Pwn'
            self.value = 1

        def move_range(self, current_state_raw, is_king_check=False):
            foreward = []
            if self.owner == 'Black':
                foreward = [chr(ord(self.position[0]) - 1) + self.position[1]]
                if self.position[0] == 'g': foreward.append(chr(ord(self.position[0]) - 2) + self.position[1])
                foreward = [x for x in foreward if x[0] in 'abcdefgh' and x[1] in '12345678'
                            and (current_state_raw[x]).owner == 'None']
                potatck = [chr(ord(self.position[0]) - 1) + str(int(self.position[1]) + 1),
                           chr(ord(self.position[0]) - 1) + str(int(self.position[1]) - 1)]
                [foreward.append(x) for x in potatck if x[0] in 'abcdefgh' and x[1] in '12345678' and
                 (current_state_raw[x]).owner == 'White']
            elif self.owner == 'White':
                foreward = [chr(ord(self.position[0]) + 1) + self.position[1]]
                if self.position[0] == 'b': foreward.append(chr(ord(self.position[0]) + 2) + self.position[1])
                foreward = [x for x in foreward if x[0] in 'abcdefgh' and x[1] in '12345678' and
                            (current_state_raw[x]).owner == 'None']
                potatck = [chr(ord(self.position[0]) + 1) + str(int(self.position[1]) + 1),
                           chr(ord(self.position[0]) + 1) + str(int(self.position[1]) - 1)]
                [foreward.append(x) for x in potatck if x[0] in 'abcdefgh' and x[1] in '12345678' and
                 (current_state_raw[x]).owner == 'Black']
            if is_king_check:
                return [move for move in potatck
                                       if move[0] in 'abcdefgh' and move[1] in '12345678']
            else:
                self.avalible_moves = {move:current_state_raw[move] for move in foreward}

    class Rook(Piece):

        def __init__(self, playerID):
            super().__init__(playerID)
            self.piece = 'Twr'
            self.value = 5

    class Bishop(Piece):
        def __init__(self, playerID):
            super().__init__(playerID)
            self.piece = 'Bsp'
            self.value = 3

    class Knight(Piece):
        def __init__(self, playerID):
            super().__init__(playerID)
            self.piece = 'Knt'
            self.value = 3

        def move_range(self, current_state_raw, *args):
            potmoves = \
                [chr(ord(self.position[0]) + 2) + str(int(self.position[1]) - 1),
                 chr(ord(self.position[0]) + 2) + str(int(self.position[1]) + 1),
                 chr(ord(self.position[0]) - 2) + str(int(self.position[1]) - 1),
                 chr(ord(self.position[0]) - 2) + str(int(self.position[1]) + 1),
                 chr(ord(self.position[0]) + 1) + str(int(self.position[1]) - 2),
                 chr(ord(self.position[0]) - 1) + str(int(self.position[1]) - 2),
                 chr(ord(self.position[0]) - 1) + str(int(self.position[1]) + 2),
                 chr(ord(self.position[0]) + 1) + str(int(self.position[1]) + 2)]
            potmoves = [x for x in potmoves if x[1] in '12345678' and '0' not in x[1:] and x[0] in 'abcdefgh']
            self.avalible_moves = {x:current_state_raw[x].owner for x in potmoves if (current_state_raw[x]).owner != self.owner}
            return [x for x in potmoves]

    class Queen(Piece):
        def __init__(self, playerID):
            super().__init__(playerID)
            self.piece = 'Qun'
            self.value = 8

    class King(Piece):
        def __init__(self, playerID):
            super().__init__(playerID)
            self.piece = 'Kng'
            self.value = 10000

    def _setup(self):
        '''
        This builds the intial chess board, calling constructors for all the chess pieces as well as a 'Dummy' piece to
        occupy empty spaces

        '''
        y = ["a", "b", "c", "d", "e", "f", "g", "h"]
        y.reverse() # sanity check this later
        for i in range(0, len(y)):
            self.board.append([y[i] + str(x) for x in range(1, 9)])
        back_row = lambda owner: [self.Rook(owner), self.Knight(owner), self.Bishop(owner),
                                  self.Queen(owner), self.King(owner), self.Bishop(owner), self.Knight(owner),
                                  self.Rook(owner)]

        for y in range(1, 9):
            self.board_state.append(back_row('Black')) if (y == 1) else \
            self.board_state.append([self.Pawn('Black') for i in range(1, 9)]) if (y == 2) else \
            self.board_state.append([self.Pawn('White') for i in range(1, 9)]) if (y == 7) else \
            self.board_state.append(back_row('White')) if (y == 8) else \
            self.board_state.append([self.Dummy() for x in range(1, 9)])

        tracker = {}
        for (a, b) in zip([xx for x in self.board for xx in x], [yy for y in self.board_state for yy in y]):
            tracker[a] = b
            if a in list(zip(*self.board))[-1]:
                self._current_state_raw.update(
                    tracker)  # the list of single dictionaries used for  tracking where everything is
                tracker = {}
            [v.getpos(self._current_state_raw) for k, v in self._current_state_raw.items()]
        self.get_current_state(self._current_state_raw)

    def _king_check_function(self):

        self.king_check[self.current_player] = []
        for k, v in self._current_state_raw.items():
            if v.owner != self.current_player and v.owner in ['Black', 'White']:
                self.king_check[self.current_player] += v.move_range(self._current_state_raw, True)
            if v.owner == self.current_player and v.piece == 'Kng':
                self.king_pos, self.king = k, v

        self.current_piece = self.king
        print(self.__str__(True,self.king_check[self.current_player]))

        if self.king_pos in self.king_check[self.current_player]:
            self.is_in_check = True
            #print('The '+self.current_player+'\'s King is in Check!')
        else:
            self.is_in_check = False

    def get_current_state(self, raw_state):

        k, v = [k for k, v in raw_state.items()], [v for k, v in raw_state.items()]
        self.current = []
        row = {}
        for i in range(0, len(k)):
            row[k[i]] = v[i]
            if len(row) == 8:
                self.current.append(row)
                row = {}

    def piece_selector(self):

        if self.pseudoAI == 'yes':
            choices = [pos for pos,piece in self._current_state_raw.items() if piece.owner == self.current_player]
            select = choices[r.randint(0, len(choices) - 1)]
            self.current_piece = self._current_state_raw[select]

    def move_selector(self,current_player):
        assert len([piece for pos, piece in self._current_state_raw.items() if piece.piece == 'Kng']) == 2

        last_state = copy.deepcopy(self._current_state_raw)
        self.current_player = current_player
        self._king_check_function()
        potential_moves = []
        hold = 0 # for the dumb ai, if no moves are avalible it counts up, if 20 is reached it's a stalemate
        if self.pseudoAI == 'yes':
            if self.is_in_check:
                self.current_piece = self.king
                potential_moves = [move for move in self.current_piece.check_if_changed(self._current_state_raw)
                                   if move not in self.king_check[self.current_player]]
                if not potential_moves: # Game over if king is in check and has no moves
                    #print('Player ' + self.current_player + ' has been forced into checkmate')
                    return -1
            else:
                while not potential_moves: # TODO see if this the selector is leading to kings dying
                    self.piece_selector()
                    potential_moves = self.current_piece.check_if_changed(self._current_state_raw) # Is this breaking the checkmate?
                    if self.current_piece.piece == 'Kng':
                        potential_moves = [move for move in potential_moves if move not in self.king_check[self.current_player]]
                        hold +=1
                    if hold == 20:
                        #print('The game is a Stalemate!')
                        return -10



            for move in potential_moves:
                dummy = copy.deepcopy(self.current_piece)
                temp = dummy.position
                dummy.position = move
                dummyboard = copy.deepcopy(self._current_state_raw)
                dummyboard[move] = dummy
                futuremoves = dummy.check_if_changed(dummyboard)
                for moves in futuremoves:
                    if moves in self.king_check[Chessgame.opponent[self.current_player]]:
                        if self._current_state_raw[move].owner == self.current_player:
                            self.move_selector(current_player)
                        else:
                            break
                else:
                    if self._current_state_raw[move].owner != self.current_player and \
                        self._current_state_raw[move].owner != 'None':
                        break
                    else:
                        move = potential_moves[r.randint(0, len(potential_moves) - 1)]
                        if self._current_state_raw[move].owner == self.current_player:
                            self.move_selector(current_player)

            if self.current_piece.piece != 'Kng' and self.Testing:
                try:
                    assert self._current_state_raw[move].piece != 'Kng'
                except:
                    self.testing_holdback.append(
                        [self.current, self.king_check[self.current_player], copy.deepcopy(self.current_piece)])
                    for i in range(-1, -5, -1):
                        self.current = self.testing_holdback[i][0]
                        print(self.testing_holdback[i][2].owner)
                        print(self)
                        print(self.__str__(True, self.testing_holdback[i][1]))
                        self.current_piece = self.testing_holdback[i][2]
                        print(self.__str__(True, self.testing_holdback[i][2].avalible_moves.keys()))
                    assert self._current_state_raw[move].piece != 'Kng'
            if self.Testing:
                self.testing_holdback.append(
                [self.current, self.king_check[self.current_player], copy.deepcopy(self.current_piece)])

            if (self.current_piece).piece == 'Pwn' and move[0] in 'ah':
                temp = self.current_piece.position
                self.current_piece = self.Queen(self.current_player)
                self.current_piece.position = move
            else:
                temp = self.current_piece.position
                self._current_state_raw[move] = self.current_piece
                self.current_piece.position = move
            self._current_state_raw[temp] = self.Dummy()
            self.get_current_state(self._current_state_raw)

            self._king_check_function()
            if self.is_in_check:
                self._current_state_raw = copy.deepcopy(last_state)
                self.move_selector(self.current_player)

    def __call__(self, *args, **kwargs):
        turn = 1
        leave = None
        opponent = {'Black':'White','White':'Black'}
        current_player = 'White'
        while leave is None:
            #print(self)
            print(current_player+'\'s Turn!')
            if current_player == 'Whie':
                emu = AlphaBeta()
                csw = copy.deepcopy(self._current_state_raw)
                emu.maxdepth = 3
                result = emu(csw,3,True,-100000,100000)
                val = max([x for x in result.keys()])
                self._current_state_raw.update({position:piece for position,piece in result[val].items() if piece.owner != 'Black'})
                self._current_state_raw.update({position: piece for position, piece in csw.items() if piece.owner == 'Black'})
                self.get_current_state(self._current_state_raw)
            else:
                leave = self.move_selector(current_player)
                self.get_current_state(self._current_state_raw)
            current_player = Chessgame.opponent[current_player]
            print(self)
            turn += 1
            if turn == 100:
                leave = -5
            else:
                turn +=1
        print(self)
        if len(self.testing_holdback) > 500:
            for i in range(-1, -5, -1):
                self.current = self.testing_holdback[i][0]
                print(self.testing_holdback[i][2].owner)
                print(self)
                print(self.__str__(True, self.testing_holdback[i][1]))
                self.current_piece = self.testing_holdback[i][2]
                print(self.__str__(True, self.testing_holdback[i][2].avalible_moves.keys()))
        if leave == -1:
            return(turn,current_player)
        elif leave == -10:
            return(turn,'Stalemate')
        elif leave ==-5: return(turn,'Maximum Turns Reached')


    def __str__(self, showmoves=False, moves=[]):

        """This just builds the actual board seen by the 'end-user' """

        rep_board = ''
        if showmoves == True:  # Outputs the board with the avalible moves for a given piece highlighted
            for dicts in self.current:
                rep_board += (
                                     "\n" + Back.LIGHTBLACK_EX + "|¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯|" + Back.RESET + "\n" + Back.LIGHTBLACK_EX + '|' + Back.RESET +
                                     (Back.LIGHTBLACK_EX + "||").join([(Back.MAGENTA if k in moves else
                                                                        Back.LIGHTBLACK_EX if k != self.current_piece.position
                                                                        else Fore.YELLOW + Back.LIGHTBLACK_EX) + ' ' + k
                                                                       + ': ' +
                                                                       (Back.MAGENTA if k in moves else
                                                                        Back.LIGHTBLACK_EX) + Style.BRIGHT + (
                                                                           Fore.YELLOW if k == (
                                                                               self.current_piece).position and self.is_in_check != True \
                                                                               else Fore.LIGHTWHITE_EX + Style.BRIGHT if i.owner == 'White'
                                                                           else Fore.BLACK + Style.BRIGHT if i.owner == 'Black'
                                                                           else Fore.RESET) + str(i)
                                                                       + ('   ' if str(i) == ' ' else '')
                                                                       + Fore.RESET for k, i in
                                                                       dicts.items()]) + Back.LIGHTBLACK_EX + "|" + Back.RESET
                                     + "\n" + Back.LIGHTBLACK_EX + "|_________||_________||_________||_________||_________||_________||_________||_________|") + Back.RESET + '\n'

        else:
            for dicts in self.current:
                rep_board += (
                                     "\n" + Back.LIGHTBLACK_EX + "|¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯|" + Back.RESET + "\n" + Back.LIGHTBLACK_EX + '|' + Back.RESET +
                                     (Back.LIGHTBLACK_EX + "||").join([Back.LIGHTBLACK_EX + ' ' + k
                                                                       + ': ' + Back.LIGHTBLACK_EX + Style.BRIGHT + (
                                                                           Fore.LIGHTWHITE_EX + Style.BRIGHT if i.owner == 'White'
                                                                           else Fore.BLACK + Style.BRIGHT if i.owner == 'Black'
                                                                           else Fore.RESET) + str(i)
                                                                       + ('   ' if str(i) == ' ' else '')
                                                                       + Fore.RESET for k, i in dicts.items()
                                                                       ]) + Back.LIGHTBLACK_EX + "|" + Back.RESET
                                     + "\n" + Back.LIGHTBLACK_EX + "|_________||_________||_________||_________||_________||_________||_________||_________|") + Back.RESET + '\n'

        return '\n' + rep_board + '\n'

class AlphaBeta(Chessgame):
    def __init__(self,isAI = True):
        super().__init__(isAI)
        self.node_value_pairs = {}

    def __call__(self, *args, **kwargs):
        _,node =  self.alphabeta(*args)
        return node
    def child_node_finder(self, node, maxing_player):

        self.current_working_node = copy.deepcopy((node))
        self.get_current_state(self.current_working_node)
        if maxing_player:
            self.current_player = 'White'
        else:
            self.current_player = 'Black'
        child_nodes = []
        moves = defaultdict(list)

        for piece in self.current_working_node.values():
            if piece.owner == self.current_player:
                if piece.check_if_changed(self.current_working_node):
                    [moves[piece].append(x) for x in [*piece.avalible_moves.keys()]]

        for piece, moves in moves.items():
            workingboard = copy.deepcopy(self.current_working_node)
            self.current_piece = piece
            piece.getpos(self.current_working_node)
            self.get_current_state(workingboard)
            if piece.piece != 'Pwn':
                pass
                #print(self.__str__(True, moves))
            for move in moves:
                workingboard = copy.deepcopy(self.current_working_node)
                pos = copy.copy(piece.position)
                workingboard[pos] = self.Dummy()
                workingboard[move] = piece
                self.get_current_state(workingboard)
                child_nodes.append(workingboard)
        return child_nodes

    def node_evaluation_heuristic(self, node):
        value = 0
        for piece in node.values():
            if piece.owner == 'White':
                if piece.move_range(node) != []:
                    value += len([*piece.avalible_moves.keys()])
            if piece.owner == 'Black':
                if piece.move_range(node) != []:
                    value -= len([*piece.avalible_moves.keys()])
        value = value//10
        for _, piece in node.items():
            value += piece.value if piece.owner == 'White' else -piece.value
        return value

    def alphabeta(self, node, depth, maxing_player, alpha, beta):
        if depth > self.maxdepth: depth = self.maxdepth
        #print(self.branch)

        if depth == 0:
            value = self.node_evaluation_heuristic(node)
            self.node_value_pairs[value] = node
            return value,self.node_value_pairs

        if maxing_player:
            value = -100000
            subnodes = self.child_node_finder(node, maxing_player)
            for nodes in subnodes:
                #self.branch[depth].append(self.alphabeta(nodes, depth - 1, False, alpha, beta))
                val,_ = self.alphabeta(nodes, depth - 1, False, alpha, beta)
                try:
                    value = max(value,val)
                except TypeError:
                    value = max(value, val[0])
                alpha = max(alpha, value)
                self.node_value_pairs[value] = nodes
                if alpha >= beta:
                    break
                else:
                    continue
            return value, self.node_value_pairs
        else:
            value = 100000
            subnodes = self.child_node_finder(node, maxing_player)
            for nodes in subnodes:
                #self.branch[depth].append(self.alphabeta(nodes, depth - 1, True, alpha, beta))
                val,__ = self.alphabeta(nodes, depth - 1, True, alpha, beta)
                value = min(value, val)
                beta = min(beta, value)
                self.node_value_pairs[value] = nodes
                if alpha >= beta:
                    break
                else: continue
            return value, self.node_value_pairs





















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