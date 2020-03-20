//
// Created by themagicalplace on 3/20/20.
//

#include "../headers/alphabeta.h"
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

AlphaBeta::AlphaBeta(string player, bool testing)
:player(player),testing(testing){

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

    while (node.next_piece() != nullptr)
    {
        Piece *piece = node.next_piece();
        std::vector<std::string> moves = piece->move_range(node.board,false);
        if (piece->owner == current_player)
            for (string &move : moves)
            {
                piece->get_position(node.board);
                next_nodes.push_back(node.spawn_child(piece,move));
            }
    }


    return next_nodes;
}

float AlphaBeta::node_evaluation_heuristic(ChessNode &node)
{
    float value{0};
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

int AlphaBeta::ab_search(ChessNode &node, int depth, bool maxing_player, int alpha, int beta) {
    return 0;
}
