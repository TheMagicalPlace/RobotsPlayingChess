//
// Created by themagicalplace on 3/20/20.
//

#ifndef PROJ1_ALPHABETA_H
#define PROJ1_ALPHABETA_H
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iterator>
#include <iostream>
#include <string>
#include <map>
#include <vector>
#include <iterator>
#include <csignal>
#include "ChessPieces.h"
template<class T>
class Alloc { };
template<class T>

using vector = std::vector<T,Alloc<T>>;
using string = std::string;
using Piece = ChessPieces::Piece;


class ChessNode
{
public:
    const std::shared_ptr<ChessNode> parent;
    const std::map<string,std::shared_ptr<ChessPieces::Piece>> board;
    const int depth;


    int index{0};       //TODO does this do anything?
    ChessNode(std::shared_ptr<ChessNode> const &prnt,int depth,std::map<string,std::shared_ptr<ChessPieces::Piece>> const &board )
    :parent(prnt),depth(depth),board(board),exit_piece(std::make_unique<Piece>("EXIT","EXIT","EXIT"))
    {

    };
    std::shared_ptr<ChessNode> spawn_child(std::shared_ptr<Piece> piece,string move);
    std::shared_ptr<Piece> next_piece();
    void set_value(double val){value=val;};
    double get_value(){ return value;};

private:

    double value{0};
    std::vector<std::shared_ptr<ChessNode>> childs{};
    std::unique_ptr<Piece> const exit_piece;
    std::_Rb_tree_const_iterator<std::pair<const std::basic_string<char>, std::shared_ptr<Piece>>> board_iter = board.begin();
};



class AlphaBeta {
public:
    std::map<std::string,std::string> opponent {{"Black","White"},{"White","Black"}};
    AlphaBeta(string player, std::map<string, std::shared_ptr<ChessPieces::Piece>> board, int dpth, bool testing);
    double call(bool maxing_player);

private:

    bool testing;
    ChessNode root_node;
    int search_depth;
    string player;
    std::vector<ChessNode*> child_node_finder(ChessNode node,int depth, bool is_maxing);
    double node_evaluation_heuristic(ChessNode &node);
    double ab_search(ChessNode* node,int depth,bool maxing_player,int alpha,int beta);



};


#endif //PROJ1_ALPHABETA_H
