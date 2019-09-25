from ChessBoard import *
import logging
from ChessPieces import *
from Player_Base import *
class RandomAI(ChessTurnABC):

    def __init__(self,player,board):
        super().__init__(player,board)
        self.testing_holdback = []
    def __call__(self,board):
        self._current_state_raw = board
        end_state = self.move_selector()
        if end_state is not None:
            return end_state


    def piece_selector(self):
        choices = [pos for pos, piece in self._current_state_raw.items() if piece.owner == self.current_player]
        select = choices[r.randint(0, len(choices) - 1)]
        self.current_piece = self._current_state_raw[select]

    def get_potential_moves(self,board_state,potential_moves = None):
        hold = 0
        if self.is_in_check:
            self.current_piece = self.king
            potential_moves = [move for move in self.current_piece.check_if_changed(board_state)
                               if move not in self.king_check[self.current_player]]
            if not potential_moves:  # Game over if king is in check and has no moves
                print('Player ' + self.current_player + ' has been forced into checkmate')
                return -1
            else:
                return potential_moves
        else:
            while not potential_moves:  # TODO see if this the selector is leading to kings dying
                self.piece_selector()
                potential_moves = self.current_piece.check_if_changed(
                    board_state)  # Is this breaking the checkmate?
                if self.current_piece.piece == 'Kng':
                    potential_moves = [move for move in potential_moves if
                                       move not in self.king_check[self.current_player]]
                    hold += 1
                if hold == 20:
                    # print('The game is a Stalemate!')
                    return -10
            else:
                return potential_moves

    def _ai_move_select(self,potential_moves):

        for move in potential_moves:
            dummy = copy.deepcopy(self.current_piece)
            temp = dummy.position
            dummy.position = move
            dummyboard = copy.copy(self._current_state_raw)
            dummyboard[move] = dummy
            futuremoves = dummy.check_if_changed(dummyboard)
            for moves in futuremoves:
                if moves in self.king_check[Chessgame.opponent[self.current_player]]:
                    if self._current_state_raw[move].owner == self.current_player:
                        self.move_selector()
                    else:
                        break
            else:
                if self._current_state_raw[move].owner != self.current_player and \
                        self._current_state_raw[move].owner != 'None':
                    break
                else:
                    move = potential_moves[r.randint(0, len(potential_moves) - 1)]
                    if self._current_state_raw[move].owner == self.current_player:
                        self.move_selector()
                    else:
                        self.current_piece.position_history.append(move)
                        return move
        return potential_moves[-1]

    def _board_logger(self,move):
        if self.current_piece != 'Kng' and self.Testing:
            try:
                assert self._current_state_raw[move].piece != 'Kng'
            except:
                self.testing_holdback.append(
                    [self.current, self.king_check[self.current_player], copy.deepcopy(self.current_piece)])
                for i in range(-1, -5, -1):
                    self.current = self.testing_holdback[i][0]
                    logging.debug(self.testing_holdback[i][2].owner)
                    logging.debug(self)
                    logging.debug(self.__str__(True, self.testing_holdback[i][1]))
                    self.current_piece = self.testing_holdback[i][2]
                    logging.debug(self.__str__(True, self.testing_holdback[i][2].avalible_moves.keys()))
                assert self._current_state_raw[move].piece != 'Kng'
        elif self.Testing:
            self.testing_holdback.append(
                [self.current, self.king_check[self.current_player], copy.deepcopy(self.current_piece)])

    def move_selector(self):

        try:
            assert len([piece for pos, piece in self._current_state_raw.items() if piece.piece == 'Kng']) == 2
        except AssertionError:
            return -999
        self._king_check_function()
        last_state = copy.copy(self._current_state_raw)
        potential_moves = self.get_potential_moves(self._current_state_raw)
        if isinstance(potential_moves,str): return potential_moves
        if potential_moves == -1:
            return - 1
        elif potential_moves == -10:
            return -10

        move = self._ai_move_select(potential_moves)
        # propogate_exception = self._board_logger(move)
        # if propogate_exception: return propogate_exception

        if (self.current_piece).piece == 'Pwn' and move[0] in 'ah':
            temp = self.current_piece.position
            self.current_piece = Queen(self.current_player)
            self.current_piece.position = move
        else:
            temp = self.current_piece.position
            self._current_state_raw[move] = self.current_piece
            self.current_piece.position = move
        self._current_state_raw[temp] = Dummy()

        self._king_check_function()
        if self.is_in_check:
            self._current_state_raw = copy.copy(last_state)
            self.move_selector()
