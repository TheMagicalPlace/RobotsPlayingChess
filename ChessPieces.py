from random import randint

class Piece():
    ''' Each subclass of the piece object has it\'s own function for checking the movment range against the
imputted move. Currently the way most of them work is by testing every appicable string combination for a given piece
(i.e. a-z,5 or a,1-5 for a rook) and discarding the ones that are invalid

'''

    opponent = {'Black':'White','White':'Black'}
    def __init__(self, playerID):
        self.owner = playerID
        self.piece = 'Undef'
        self.value = 0
        self.avalible_moves = {}
        self.kc_moves = {}
        self.position_history = []
        self.rng = randint(1,1000)


    def __eq__(self, other):
        return self.piece == other

    def __hash__(self):
        return hash((self.owner,self.piece,self.rng))

    def check_if_changed(self, current_board, is_king_check=False):
        """checks if the pieces move range has changed since the last check by checking if the spaces of the prev.
        moves have the same piece as before"""
        self.move_range(current_board,is_king_check)

        # checks for moves if none were found last time
        if not self.avalible_moves:
            self.move_range(current_board, is_king_check)
            return [*self.avalible_moves.keys()]
        for move in self.avalible_moves.keys():
            if current_board[move] == self.avalible_moves[move]:
                continue
            else:
                self.move_range(current_board, is_king_check)
                break

        return [*self.avalible_moves.keys()]

    def __str__(self):
        return self.piece + ' '  # self.owner + self.piece

    def getpos(self, current_state_raw):
        """Updates the board position of the piece"""
        self.position = "".join([k for k, v in current_state_raw.items() if self is current_state_raw[k]])

    def move_range(self, current_state_raw, is_king_check=False):
        """finds avalible moves based on what piece it is, knights and pawns have their own move rules in their \
        respective classes"""
        up_right, up_left, down_right, down_left, up, down, left, right = \
            self.position, self.position, self.position, self.position, self.position, self.position, self.position, self.position
        if self.piece == 'Twr':
            up_right, up_left, down_right, down_left = -1, -1, -1, -1
        elif self.piece == 'Bsp':
            up, down, left, right = -1, -1, -1, -1
        moves = []
        for i in range(1, 8):

            # -1 is used to indicate that the last checked spot is the furthest move in that direction
            if up_left == up_right == down_left == down_right == up == down == left == right == -1: break
            up_right = (chr(ord(self.position[0]) + i) + str(int(self.position[1]) + i)) if up_right != -1 else -1
            up_left = (chr(ord(self.position[0]) - i) + str(int(self.position[1]) - i)) if up_left != -1 else -1
            down_right = (chr(ord(self.position[0]) + i) + str(int(self.position[1]) - i)) if down_right != -1 else -1
            down_left = (chr(ord(self.position[0]) - i) + str(int(self.position[1]) + i)) if down_left != -1 else -1
            up = (chr(ord(self.position[0]) + i) + str(int(self.position[1]))) if up != -1 else -1
            down = (chr(ord(self.position[0]) - i) + str(int(self.position[1]))) if down != -1 else -1
            left = (chr(ord(self.position[0])) + str(int(self.position[1]) - i)) if left != -1 else -1
            right = (chr(ord(self.position[0])) + str(int(self.position[1]) + i)) if right != -1 else -1

            #
            next = [str(up_right), str(up_left), str(down_right),
                    str(down_left), str(up), str(down), str(left), str(right)]
            pots = [x for x in next if x[0] in 'abcdefgh' and x[1] in '12345678']

            # all moves are looked at when a king is in check
            if is_king_check:
                pots = [x for x in pots]
            else:
                pots = [x for x in pots if (current_state_raw[x]).owner != self.owner]
            for x in pots:
                # accounts for opposing pieces as an avalible move & blocker
                if (current_state_raw[x]).owner == self.opponent[self.owner]:
                    #kings can only move one space
                    if is_king_check:
                        if (current_state_raw[x]).piece == 'Kng':
                            moves.append(x)
                    else:
                        moves.append(x)
                        pots.remove(x)
            [moves.append(x) for x in pots]

            #checking next spaces
            for x in next:
                if is_king_check:
                    next[next.index(x)] = -1 if x not in pots else -1 \
                        if current_state_raw[x].owner == self.owner else x
                else:
                    next[next.index(x)] = -1 if x not in pots else x

            if self.piece != 'Kng':
                up_right, up_left, down_right, down_left, up, down, left, right = next
            else:
                up_right, up_left, down_right, down_left, up, down, left, right = -1, -1, -1, -1, -1, -1, -1, -1
        if is_king_check:
            return moves
        else:
            self.avalible_moves = {move: current_state_raw[move] for move in moves} if moves else {}


class Dummy(Piece):
    """
    This is the object used in blank spaces, given that it doesn't really take up any memory it's worth it for
    the convenience alone
    """

    def __init__(self):
        self.owner = 'None'
        self.piece = "Not a Piece"
        self.value = 0
        self.rng = randint(1,100)

    def __str__(self):
        return ' '


class Pawn(Piece):
    def __init__(self, playerID):
        super().__init__(playerID)
        self.piece = 'Pwn'
        self.value = 1 # heuristic val for AI

    def move_range(self, current_state_raw, is_king_check=False):
        """Pawns have special move rules"""
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
            # pawns can only  attackdiagonallyy
            return [move for move in potatck
                    if move[0] in 'abcdefgh' and move[1] in '12345678']
        else:
            self.avalible_moves = {move: current_state_raw[move] for move in foreward}


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
        # knights have special move rules
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
        self.avalible_moves = {x: current_state_raw[x].owner for x in potmoves if
                               (current_state_raw[x]).owner != self.owner}
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
        self.value = 100000 # functionally infinite