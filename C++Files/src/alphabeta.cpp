//
// Created by themagicalplace on 3/20/20.
//

#include "../headers/alphabeta.h"
#include <utility>
#include <vector>
ChessNode::ChessNode(const ChessNode *, int depth,const std::map<string, Piece *> &board) {

}

ChessNode ChessNode::spawn_child( Piece* piece, string move) {
    std::map<string, Piece *> nboard{this->board};

    // debugging invalid piece positions
    if (piece->position.length() > 2)
        std::cout << piece->position;
    string old = piece->position;
    nboard[move] = piece;
    *nboard[old] = Piece("None",old,"NA");
    ChessNode new_node = ChessNode(this, this->depth+1, nboard);
    new_node.parent = this;
    this->childs.push_back(&new_node);
    return new_node;
}

Piece* ChessNode::next_piece() {
    if (board_iter != board.end())
    {
        Piece * pce = board_iter->second;       // get the piece
        board_iter++;                           // and advance the iterator
        return pce;
    }
    else
    {

        return nullptr;                         // return null if exhausted
    }


}

AlphaBeta::AlphaBeta(string player,const std::map<string,Piece *> &board,int dpth,bool testing)
:player{std::move(player)},testing{testing},root_node{ChessNode(nullptr,dpth,board)},search_depth{dpth}{

}

std::vector<ChessNode> AlphaBeta::child_node_finder(ChessNode &node, int depth, bool is_maxing) {

    // container for found children
    std::vector<ChessNode> next_nodes{} ;

    // determines which players pieces moves are examined
    string current_player;
    if (is_maxing)
        current_player = player;
    else
        current_player = opponent[player];


    // Implemented to be semi-analogous to a python generator, what this does is create the child nodes for each
    // piece at a time, therefore if the main alpha-beta search breaks early no time will have been wasted in
    // generating extraneous child nodes for the other pieces.

    Piece *piece = node.next_piece();
    if (piece!= nullptr)
    {

        std::vector<std::string> moves = piece->move_range(node.board,false);
        if (piece->owner == current_player)
            for (string &move : moves)
            {
                piece->get_position(node.board);
                next_nodes.push_back(node.spawn_child(piece,move));
            }
    }

    // returns the empty vector
    return next_nodes;
}

double AlphaBeta::node_evaluation_heuristic(ChessNode &node)
{
    double value{0};
    while (node.next_piece() != nullptr)
    {
        Piece *piece = node.next_piece();
            if (piece->owner == player)
            {
                value += piece->get_value();
            }
            else if (piece->owner == piece->opponent[piece->owner])
            {
            value -= piece->get_value();
            }
    }
    return value;
}

double AlphaBeta::ab_search(ChessNode &node, int depth, bool maxing_player, int alpha, int beta) {
    double value;

    // at maximum depth score board and assign value to node
    if (depth == 0)
    {
        value = node_evaluation_heuristic(node);
        node.set_value(value);
        return value;
    }

    std::vector<ChessNode> nodes = child_node_finder(node,depth,maxing_player);
    if (maxing_player)
    {
        value= -100000;

        // to reduce time+memory complexity, the child nodes are generated semi-lazily, that way if pruning occurs
        // no time would be wasted on generating unexamined child nodes
        while(not nodes.empty())
        {
            // I say semi-randomly because its not a true iterator, the ChessNode class creates an iterator of the board
            // map and returns the pointer for the next piece when called, however all moves for that piece have nodes
            // created for them, which can lead to some waste if pruning occurs before all returned nodes are examined
            for(auto &n : nodes)
            {
                double val = ab_search(n,depth-1,false,alpha,beta);
                value = std::fmax(val,value);
                alpha = std::fmax(alpha,value);
                if (alpha >=beta)
                {
                    node.set_value(value);
                    return value;
                }
            }

            // getting next nodes to examine
            nodes= child_node_finder(node,depth,maxing_player);

        }
    }
    else
    {
        value =100000;
        while(not nodes.empty())
        {
            for(auto &n : nodes)
            {
                double val = ab_search(n,depth-1,true,alpha,beta);
                value = std::fmin(val,value);
                beta = std::fmin(beta,value);
                if (alpha >=beta)
                {
                    node.set_value(value);
                    return value;
                }
            }
            nodes= child_node_finder(node,depth,maxing_player);
        }
    }

    // If no pruning is done set node value & return
    node.set_value(value);
    return value;
}

double AlphaBeta::call(bool maxing_player) {
    double result = ab_search(root_node,maxing_player,search_depth,-100000,100000);
    return result;
}
