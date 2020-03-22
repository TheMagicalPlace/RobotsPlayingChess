//
// Created by themagicalplace on 3/20/20.
//

#ifndef PROJ1_ALPHABETA_H
#define PROJ1_ALPHABETA_H

#include <iostream>
#include <string>
#include <map>
#include <vector>
#include <iterator>
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
    std::map<string,Piece *> board;
    int index{0};       //TODO does this do anything?
    ChessNode(const ChessNode * parent,int depth,std::map<string,Piece *> board );
    ChessNode spawn_child( Piece *piece,string move);
    Piece * next_piece();
    void set_value(double val){value=val;};
    double get_value(){ return value;};

private:
    double value{0};       // initializer value
    int depth{};
    std::vector<ChessNode *> childs{};
    ChessNode *parent{};
    std::map<string,Piece *>::iterator board_iter;
    int iter_count{0};
};



class AlphaBeta {
public:
    std::map<std::string,std::string> opponent {{"Black","White"},{"White","Black"}};
    AlphaBeta(string player,std::map<string,Piece *> &board,int dpth,bool testing);
    double call(bool maxing_player);

private:

    bool testing;
    ChessNode root_node;
    int search_depth;
    string player;
    std::vector<ChessNode> child_node_finder(ChessNode &node,int depth, bool is_maxing);
    double node_evaluation_heuristic(ChessNode &node);
    double ab_search(ChessNode &node,int depth,bool maxing_player,int alpha,int beta);



};


#endif //PROJ1_ALPHABETA_H
