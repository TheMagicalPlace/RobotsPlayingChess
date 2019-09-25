import random as r
from abc import abstractmethod
from collections import defaultdict

class ChessTurnABC:

    def __init__(self,player,working_board):
        self.current_player = player
        self._current_state_raw = working_board
        self.king_check = defaultdict(list)

    @abstractmethod
    def piece_selector(self):
        pass

    @abstractmethod
    def move_selector(self):
        pass

    def _king_check_function(self):

        for k, v in self._current_state_raw.items():
            if v.owner != self.current_player and v.owner in ['Black', 'White']:
                self.king_check[self.current_player] += v.move_range(self._current_state_raw, True)
            if v.owner == self.current_player and v.piece == 'Kng':
                self.king_pos, self.king = k, v

        self.current_piece = self.king
        if self.king_pos in self.king_check[self.current_player]:
            self.is_in_check = True
        else:
            self.is_in_check = False