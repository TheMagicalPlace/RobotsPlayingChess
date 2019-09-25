
from collections import defaultdict
from ChessBoard import *


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
                workingboard[pos] = Dummy()
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
