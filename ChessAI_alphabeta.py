import copy
from collections import defaultdict
from ChessBoard import Chessgame
from Player_Base import *
from ChessPieces import *

class ChessNode(Chessgame):

    def __init__(self,depth,board,value=None,parent=None):
        self.parent = parent
        self.depth = depth
        self.value = value
        self.board = board
        self.index = 0
        self.children = []
        self.get_current_state(board)

    def __ge__(self, other):
        return self.value >= other
    def __le__(self, other):
        return self.value <= other
    def __lt__(self, other):
        return self.value < other
    def __gt__(self, other):
        return self.value > other

    def __call__(self):
        return self.board
    def __iter__(self):
        return next(self)
    def items(self):
         return self.board.items()
    def __getitem__(self, key):
        return self.board[key]
    def __setitem__(self, key, value):
        self.board[key] = value

    def __next__(self):
        subs = (value for _, value in self.board.items())
        while True:
            try:
                yield next(subs)
            except StopIteration:
                break


class AlphaBeta(ChessTurnABC,Chessgame):
    opponent = {'Black': 'White', 'White': 'Black'}
    def __init__(self,player):
        super(ChessTurnABC).__init__()
        self.node_value_pairs = {}
        self.player = player
    def __call__(self, root,depth):
        self.root_node = ChessNode(depth,root)
        self.alphabeta(self.root_node,depth,True,-100000,100000)
        return max(self.root_node.children).board

    def child_node_finder(self, node, depth,is_maxing):

        self.current_working_node = node
        self.get_current_state(self.current_working_node)
        child_nodes = []
        moves = defaultdict(list)
        if is_maxing:
            current_player = self.player
        else:
            current_player=self.opponent[self.player]
        for piece in self.current_working_node:
            piece.getpos(self.current_working_node)
            if piece.owner == current_player:
                if piece.check_if_changed(self.current_working_node):
                    [moves[piece].append(x) for x in [*piece.avalible_moves.keys()]]

        for piece, moves in moves.items():
            self.current_piece = piece
            for move in moves:
                workingboard = copy.copy(self.current_working_node.board)
                workingboard[piece.position],workingboard[move] = Dummy(),piece
                child_nodes.append(ChessNode(depth,workingboard,parent=node))
                child_nodes[-1].parent.children.append(child_nodes[-1])
        return child_nodes

    def node_evaluation_heuristic(self, node):
        value = 0
        for _,piece in node.items():
            if piece.owner == self.player:
                if piece.move_range(node) != []:
                    value += len([*piece.avalible_moves.keys()])
            if piece.owner == self.opponent[self.player]:
                if piece.move_range(node) != []:
                    value -= len([*piece.avalible_moves.keys()])
        value = value//10
        for _, piece in node.items():
            value += piece.value if piece.owner == self.player else -piece.value
        return value

    def alphabeta(self, node, depth, maxing_player, alpha, beta):


        if depth == 0:
            value = self.node_evaluation_heuristic(node)
            node.parent.children.append(ChessNode(0,node.board,value=value))
            return value

        if maxing_player:
            value = -100000

            subnodes = self.child_node_finder(node,depth,maxing_player)
            node.children = subnodes
            for nodes in subnodes:
                #self.branch[depth].append(self.alphabeta(nodes, depth - 1, False, alpha, beta))
                val = self.alphabeta(nodes, depth - 1, False, alpha, beta)
                try:
                    value = max(value,val)
                except TypeError:
                    value = max(value, val[0])
                alpha = max(alpha, value)
                nodes.value = value
                if alpha >= beta:
                    break
                else:
                    continue
            return value
        else:
            value = 100000
            subnodes = self.child_node_finder(node, depth,maxing_player)
            for nodes in subnodes:
                #self.branch[depth].append(self.alphabeta(nodes, depth - 1, True, alpha, beta))
                val = self.alphabeta(nodes, depth - 1, True, alpha, beta)
                value = min(value, val)
                beta = min(beta, value)
                nodes.value = value
                if alpha >= beta:
                    break
                else: continue
            return value


if __name__ == '__main__':


    t = Chessgame()
    a = AlphaBeta('White')
    a(t._current_state_raw,5)
    print(a)