from pathlib import Path

if __name__ == '__main__':
    import time
    import sys, os

    # TODO this needs to be changed for linux
    sys.path.append(os.path.join(Path(os.getcwd()).parent,'build_files','build','lib.win-amd64-3.8'));

import pythonCPPinterop as PCPPI
import copy
from collections import defaultdict
from PythonFiles.ChessBoard import Chessgame
from PythonFiles.Player_Base import *
from PythonFiles.ChessPieces import *
from multiprocessing import Queue,Pool
from queue import Queue
from typing import Dict,Tuple


class vars:
    """class that holds the depth of the MinMax search (i.e. how many rounds to look ahead) for easy adjustment"""
    player = 'White'
    depth = 3

def child_process(node,player,depth):
    """Spawns an instance of the AlphaBeta class with depth of vars.depth for the node given to it, with
    the nodes themselves being created in MultiprocessAB"""
    abspawn = AlphaBeta(player)
    return abspawn.call_multiprocess(node,maxing=False,depth=depth)

def child_process_cpp(node,player,depth):
    board_string = node.convert_to_string();
    value = PCPPI.PythonCPPRunAlphabeta(board_string,depth,player)
    node.value = value
    return node

class ChessNode():
    """info container for each node in the MinMax tree with the 'board value' (how desirable a board state is)
     initially set to nothing and later calculated based on its child nodes"""

    def __init__(self,depth,board,value=None,parent=None):
        self.parent = parent # the parent node / the board state one move back
        self.depth = depth
        self.value = value # the value of the board, calculated via a heuristic
        self.board = board
        self.index = 0
        self.children = None

    def convert_to_string(self):

        str = ""
        for k,v in self.board.items():
            pos = k + ' '
            piece = v.piece + ' '
            owner = v.owner + ' '
            str +=pos+piece+owner+' '
        return str

    # Comparison operators for alpha-beta pruning and finding min/max vals
    def __ge__(self, other):
        return self.value >= other
    def __le__(self, other):
        return self.value <= other
    def __lt__(self, other):
        return self.value < other
    def __gt__(self, other):
        return self.value > other


    def __call__(self) -> Dict[str,Piece]:
        """returns the board state as a dict"""
        return self.board
    def __iter__(self):
        """returns a Piece based object """
        return next(self)

    def items(self):
         return self.board.items()
    def __getitem__(self, key):
        return self.board[key]
    def __setitem__(self, key, value):
        self.board[key] = value

    def __next__(self):
        subs = (value for _, value in self.board.items())

        # runs through all of the Piece nodes and terminates once exhausted
        while True:
            try:
                yield next(subs)
            except StopIteration:
                break


class AlphaBeta(ChessTurnABC,Chessgame):
    """A Chess 'AI' that generates its optimal move via an implimentation of the MinMax algorithm with alpha-beta pruning.
    Inherits movw restriction rules from ChessTurnABC and board parsing from Chessgame"""
    type = 'alpha-beta'
    opponent = {'Black': 'White', 'White': 'Black'}

    def __init__(self,player):
        super(ChessTurnABC).__init__()
        self.player = player


    def call_multiprocess(self,node,maxing=False,depth=vars.depth):
        self.root_node = node
        self.alphabeta(self.root_node, depth, maxing, -100000, 100000)
        optimal_node = min([child for child in self.root_node.children if child.value is not None])
        return optimal_node.parent



    def __call__(self,root : Dict[str,Piece],depth : int =vars.depth,maxing=True):

        self.root_node = ChessNode(depth,board=root) # creates the initial node, representing the current game state
        self.alphabeta(self.root_node,depth,maxing,-100000,100000)
        self._current_state_raw = max([child for child in self.root_node.children if child.value is not None]).board
        return self._current_state_raw

    def call_cpp(self,root : Dict[str,Piece],depth : int =vars.depth,maxing=True):
        self.root_node = ChessNode(depth,board=root) # creates the initial node, representing the current game state
        childs = self.child_node_finder(self.root_node,depth,True)
        self.root_node.children = childs
        for child in childs:
            child.value = PCPPI.PythonCPPRunAlphabeta(child.convert_to_string(),depth-1,self.player)
        self._current_state_raw = max([child for child in self.root_node.children if child.value is not None]).board
        return self._current_state_raw

    def child_node_finder(self, node : ChessNode, depth : int,is_maxing : bool) ->Tuple[ChessNode]:
        """finds all the possible child nodes / avalible moves for a given board state and depth, with
         the AIs piece color being moves with is_maxing is True, and the AIs opponents color otherwise"""
        self.current_working_node = node # the node for which to find child nodes
        child_nodes = []
        moves = defaultdict(list) # a dict of piece:move(s)

        # determines what pieces to find moves for
        if is_maxing:
            current_player = self.player
        else:
            current_player=self.opponent[self.player]

        for piece in self.current_working_node:
            piece.getpos(self.current_working_node) # tells each Piece object where it currently is on the board
            if piece.owner == current_player:
                # move_range inherited from Chessgame, the piece finds its own moves based on the board state
                piece.move_range(self.current_working_node)
                [moves[piece].append(x) for x in [*piece.avalible_moves.keys()]]

        for piece, moves in moves.items():
            self.current_piece = piece # holdover for printing a visual representation of the pieces' possible moves

            # creates a shallow copy of the board state, moves the piece, and creates a new ChessNode for that board
            for move in moves:
                workingboard = copy.copy(self.current_working_node.board)
                workingboard[piece.position],workingboard[move] = Dummy(),piece
                child_nodes.append(ChessNode(depth,workingboard,parent=node))
        return tuple(child_nodes)

    def node_evaluation_heuristic(self, node: ChessNode) -> int:
        """determines the value of the board state based on the pieces and moves available"""
        value = 0
        for piece in node:
            if piece.owner == self.player:
                value += piece.value # add the values of the players remaining pieces
                if piece.move_range(node) != []:
                    value += len([*piece.avalible_moves.keys()])*0.1 # add the values of the moves avalible to that piece
            if piece.owner == self.opponent[self.player]:
                value -= piece.value # subtract the value of the opponents pieces
                if piece.move_range(node) != []:
                    value -= len([*piece.avalible_moves.keys()])*0.1 # and avalible moves
        return value

    def alphabeta(self, node:ChessNode, depth:int, maxing_player:bool, alpha:int, beta:int):
        """driving function for the AI, recursively finds the best board state based on minimizing/maximizing the
        ChessNode.value (max for AI, min for opponent) for the children of a given node and then
        assignes the parent node that value and then returns the value to the layer above it(depth+1) """

        # at maximum depth the value for the node is calculated and assigned
        if depth == 0:
            value = self.node_evaluation_heuristic(node)
            node.value = value
            return value

        if maxing_player:
            # Trying to find the best board state for the AI
            value = -100000
            subnodes = self.child_node_finder(node,depth,maxing_player)
            node.children = subnodes
            for nodes in subnodes:
                val = self.alphabeta(nodes, depth - 1, False, alpha, beta)
                try:
                    value = max(value,val)
                except TypeError:
                    value = max(value, val[0])
                alpha = max(alpha, value)
                node.value = value

                # if the alpha value is greater than the beta value, then the branch is terminated as this indicates
                # that further nodes are not viable
                if alpha >= beta:
                    break
                else:
                    continue
            return value
        else:
            # Trying to find the best board state for the opponent
            value = 100000
            subnodes = self.child_node_finder(node, depth,maxing_player)
            node.children = subnodes
            for nodes in subnodes:
                val = self.alphabeta(nodes, depth - 1, True, alpha, beta)
                value = min(value, val)
                beta = min(beta, value)
                node.value = value
                if alpha >= beta:
                    break
                else: continue
            return value

class MultiprocessAB(AlphaBeta):
    """this class allows the use of multiple cores to for faster computation time"""
    def __init__(self, player, root,depth=vars.depth):
        super().__init__(player)
        self.depth = depth
        self.root_node = ChessNode(depth,root)
        self.mp_childs = self.child_node_finder(self.root_node,depth-1,True) # finds the children for the initial board
        self.root_node.children = tuple(self.mp_childs)


    def __call__(self):
        """ Executes a multiprocess Alpha-Beta minmax search via a custom C++ implementation of the search algorithm"""
        with Pool(5) as p:
            data = p.starmap(child_process_cpp, [(child,self.player,self.depth-2) for child in self.mp_childs]) # runs an instance of AlphaBeta for each child node
        self._current_state_raw=max(data).board

    def call_python(self):
        """Legacy - for testing only"""
        with Pool(5) as p:
            data = p.starmap(child_process, [(child,self.player,self.depth-2) for child in self.mp_childs]) # runs an instance of AlphaBeta for each child node
            self._current_state_raw=max(data).board

if __name__ == '__main__':
    import time
    import sys, os
    sys.path.append(os.path.join(os.getcwd(),'build_files','build','lib.win-amd64-3.8'));
    t = Chessgame()
    initial = time.time()


    for i in range(4,8):

        a = MultiprocessAB('Black',t._current_state_raw,depth=i)
        t0  = time.time()
        a()
        print(f'Run Time at depth {i} using multiprocessing and C++ : {time.time() - t0:08f}\n')


        a = MultiprocessAB('Black',t._current_state_raw,depth=i)
        t0  = time.time()
        a.call_python()
        print(f'Run Time at depth {i} using multiprocessing and Python Search : {time.time() - t0:08f}\n')


        a = AlphaBeta('Black')
        t0  = time.time()
        a.call_cpp(t._current_state_raw,i,True)
        print(f'Run Time at depth {i} using single process and C++ : {time.time() - t0:08f}\n')


        #a = AlphaBeta('Black')
        #t0  = time.time()
        #a(t._current_state_raw,i,True)
        #print(f'Run Time at depth {i} using single process and Python Search : {time.time() - t0:08f}\n')


