"""


"""





import copy
import random as r
from collections import defaultdict

from colorama import Fore, Back, Style


class Chessgame():
    Names = ['Rook', 'Knight', 'Bishop',
             'Queen', 'King', 'Pawn']

    def __init__(self, isAI):
        self.isAI = isAI
        self.board = []
        self.board_state = []
        self.current = []
        self._current_state_raw = {}
        self.setup()

    def setup(self):
        if self.isAI == False:
            self._board_setup()  # sets up the starting board
            self._position_setup()  # initiallizes the chess piece objects
            self.king_check = {'Black': [], 'White': []}
            self.turn_count = 0

    class Dummy():

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

        def getpos(self, current_state_raw):
            self.position = "".join([k for k, v in current_state_raw.items() if self == current_state_raw[k]])

    class Piece():
        ''' Each subclass of the piece object has it\'s own function for checking the movment range against the
    imputted move. Currently the way most of them work is by testing every appicable string combination for a given piece
    (i.e. a-z,5 or a,1-5 for a rook) and discarding the ones that are invalid

    '''
        def __init__(self, playerID):
            self.owner = playerID
            self.piece = 'Undef'
            self.value = 0

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
                if up_left == up_right == down_left == down_right == up == down == left == right == -1: return moves
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
                pots = [x for x in pots if (current_state_raw[x]).owner != self.owner]
                for x in pots:
                    if (current_state_raw[x]).owner != self.owner and str(current_state_raw[x]) != ' ':
                        if is_king_check:
                            if (current_state_raw[x]).piece == 'Kng':
                                moves.append(x)
                            else:
                                moves.append(pots.pop(pots.index(x)))
                for x in pots: moves.append(x)
                for x in next: next[next.index(x)] = -1 if x not in pots else x
                if self.piece != 'Kng':
                    up_right, up_left, down_right, down_left, up, down, left, right = next
                else:
                    up_right, up_left, down_right, down_left, up, down, left, right = -1,-1,-1,-1,-1,-1,-1,-1

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
            if self.owner == 'White':
                foreward = [chr(ord(self.position[0]) + 1) + self.position[1]]
                if self.position[0] == 'b': foreward.append(chr(ord(self.position[0]) + 2) + self.position[1])
                foreward = [x for x in foreward if x[0] in 'abcdefgh' and x[1] in '12345678' and
                            (current_state_raw[x]).owner == 'None']
                potatck = [chr(ord(self.position[0]) + 1) + str(int(self.position[1]) + 1),
                           chr(ord(self.position[0]) + 1) + str(int(self.position[1]) - 1)]
                [foreward.append(x) for x in potatck if x[0] in 'abcdefgh' and x[1] in '12345678' and
                 (current_state_raw[x]).owner == 'Black']
            if is_king_check:
                return potatck
            else:
                return foreward

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
            potmoves = [x for x in potmoves if (current_state_raw[x]).owner != self.owner]
            return potmoves

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

    def _king_check_function(self):

        self.king_check[self.current_player] = []
        for k, v in self._current_state_raw.items():
            if v.owner != self.current_player and v.owner in ['Black', 'White']:
                self.king_check[self.current_player] += v.move_range(self._current_state_raw, True)
            if v.owner == self.current_player and v.piece == 'Kng':
                self.king_pos, self.king = k, v

        if self.king_pos in self.king_check[self.current_player]:
            self.is_in_check = True
        else:
            self.is_in_check = False

    def _position_setup(self):
        '''
        This builds the intial chess board, calling constructors for all the chess pieces as well as a 'Dummy' piece to
        occupy empty spaces

        '''
        back_row = lambda owner: [self.Rook(owner), self.Knight(owner), self.Bishop(owner),
                                  self.Queen(owner), self.King(owner), self.Bishop(owner), self.Knight(owner),
                                  self.Rook(owner)]

        for y in range(1, 9):
            self.board_state.append(back_row('White')) if (y == 1) else \
                self.board_state.append([self.Pawn('White') for i in range(1, 9)]) if (y == 2) else \
                    self.board_state.append([self.Pawn('Black') for i in range(1, 9)]) if (y == 7) else \
                        self.board_state.append(back_row('Black')) if (y == 8) else \
                            self.board_state.append([self.Dummy() for x in range(1, 9)])
        tracker = {}
        for (a, b) in zip([xx for x in self.board for xx in x], [yy for y in self.board_state for yy in y]):
            tracker[a] = b
            # TODO fix the updater so it can properly print out strings
            if a in list(zip(*self.board))[-1]:
                self._current_state_raw.update(
                    tracker)  # the list of single dictionaries used for  tracking where everything is
                tracker = {}
            [v.getpos(self._current_state_raw) for k, v in self._current_state_raw.items()]
        self.get_current_state(self._current_state_raw)

    def _board_setup(self):
        y = ["a", "b", "c", "d", "e", "f", "g", "h"]
        for i in range(0, len(y)):
            self.board.append([y[i] + str(x) for x in range(1, 9)])

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
            choices = [k for k, v in self._current_state_raw.items() if v.owner == self.current_player]
            select = choices[r.randint(0, len(choices) - 1)]
            self.current_piece = self._current_state_raw[select]
            return

        while 1 == 1:

            select = input('What piece would you like to move ?\n'
                           '(select piece from coordinates or 0 to exit)')
            if select == '0': exit()
            if select not in self._current_state_raw.keys():
                print('Invalid cordinates')
                continue
            elif (self._current_state_raw[select]).owner != self.current_player:
                print('This is not you piece!')
            else:
                self.current_piece = self._current_state_raw[select]
                return

    def move_selector(self):
        # TODO - Allow other pieces to be used to get the king out of check(if in check)
        potential_moves = self.current_piece.move_range(self._current_state_raw)

        if self.pseudoAI == 'yes':
            if self.is_in_check:
                self.current_piece = self.king
                potential_moves = (self.current_piece).move_range(self._current_state_raw)
                potential_moves = [x for x in potential_moves if x not in self.king_check[self.current_player]]
                if not potential_moves:
                    print('Player ' + self.current_player + ' has been forced into checkmate')
                    leave = 1
                    return leave
            elif (self.current_piece).piece == 'Kng':
                potential_moves = (self.current_piece).move_range(self._current_state_raw)
                potential_moves = [x for x in potential_moves if x not in self.king_check[self.current_player]]
                while not potential_moves:
                    self.piece_selector()
                    potential_moves = (self.current_piece).move_range(self._current_state_raw)
            else:
                while not potential_moves:
                    self.piece_selector()
                    potential_moves = (self.current_piece).move_range(self._current_state_raw)
            # print(s.__str__(True, potential_moves))

            for x in potential_moves:
                if (self._current_state_raw[x]).owner != self.current_player and self._current_state_raw[x] != 'None':
                    move = x
                else:
                    move = potential_moves[r.randint(0, len(potential_moves) - 1)]
            if (self.current_piece).piece == 'Pwn':
                if move[0] in 'ah':
                    holder = self.current_piece.position
                    self.current_piece = self.Queen(self.current_player)
                    (self.current_piece).position = holder
            replacer = self.current_piece.position
            self._current_state_raw[move] = self.current_piece
            (self.current_piece).position = move
            self._current_state_raw[replacer] = self.Dummy()
            for dict in self.current:
                for x in dict.keys(): dict[x] = self._current_state_raw[x]
            if self.pseudoAI == 'no': print(self)
            return

        #TODO match this section with the one above
        while 1 == 1:
            if self.is_in_check:
                self.current_piece = self.king
                potential_moves = (self.current_piece).move_range(self._current_state_raw)
                if not potential_moves:
                    exit('Player' + self.current_player + 'Has been forced into checkmate')
            move = input('Select where you would like to move this piece \n'
                         'or imput \'moves\' to show possible moves ')
            if move == '0':
                exit(print('Thanks for playing!'))
            if move == 'moves':
                print(s.__str__(True, potential_moves))
            elif move not in potential_moves:
                print('This is not a valid destination')
            else:
                confirm = input('Confirm move' + (self.current_piece).position + '--->' + move)
                if 'y' in confirm:
                    self._current_state_raw[move] = self.current_piece
                    self._current_state_raw[(self.current_piece).position] = self.Dummy()
                    for dict in self.current:
                        for x in dict.keys(): dict[x] = self._current_state_raw[x]

                    print(self)
                    return
                    # this will likely be how changes are incorporated


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

