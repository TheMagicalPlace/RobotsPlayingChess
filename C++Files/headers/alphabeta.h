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
#include <iterator>
#include <csignal>
#include <cstdlib>
#include <algorithm>
#include <vector>
#include <utility>

#include "ChessPieces.h"

#include <iso646.h>


template<class T>
class Alloc { };
template<class T>

using vector = std::vector<T,Alloc<T>>;
using string = std::string;
using Piece = ChessPieces::Piece;



class ChessNode
{
public:

    const std::map<string,std::shared_ptr<ChessPieces::Piece>> board;

    ChessNode(int depth,std::map<string,std::shared_ptr<ChessPieces::Piece>> const &board )
    :depth(depth),board(board),exit_piece(std::make_shared<Piece>("EXIT","EXIT","EXIT"))
    {

        transform(board.begin(), board.end(), back_inserter(board_iter), [](const std::map<string,std::shared_ptr<ChessPieces::Piece>>::value_type& val){return val.second;} );

    };

    virtual ~ChessNode(){
        board_iter.clear();
        childs.clear();
        board_iter.clear();
    };

    std::shared_ptr<ChessNode> spawn_child(std::shared_ptr<Piece> const &piece, string move);
    std::shared_ptr<Piece> next_piece();

    void set_value(double val){value=val;};
    double get_value(){ return value;};

private:
    //const std::shared_ptr<ChessNode> parent;
    //std::unique_ptr<ChessNode> this_ptr= std::unique_ptr<ChessNode>(this) ;
    const int depth;
    const std::shared_ptr<Piece> exit_piece;
    double value{0};
    int index{0};

    std::vector<std::shared_ptr<ChessNode>> childs{};
    std::vector<std::shared_ptr<ChessPieces::Piece>> board_iter;

};



class AlphaBeta {
public:
    const std::map<std::string,std::string> opponent {{"Black","White"},{"White","Black"},{"None","None"}};

    AlphaBeta(string player, std::map<string, std::shared_ptr<ChessPieces::Piece>> const board, int dpth, bool testing)
        :player{std::move(player)},
        testing{testing},
        board(board),
        search_depth{dpth}
    {

    };
    virtual ~AlphaBeta()
    {


    };
    double call(bool maxing_player);

private:
    const std::map<string, std::shared_ptr<ChessPieces::Piece>> board;
    const bool testing;
    const int search_depth;
    const string player;
    const std::shared_ptr<ChessNode> root_node {std::make_shared<ChessNode>(search_depth,board)};


    std::vector<std::shared_ptr<ChessNode>> child_node_finder(std::shared_ptr<ChessNode> const &node, int depth, bool is_maxing) const;
    double node_evaluation_heuristic(std::shared_ptr<ChessNode> const &node, bool is_maxing);
    double ab_search(std::shared_ptr<ChessNode> const &node,int depth,bool maxing_player,int alpha,int beta);



};


#endif //PROJ1_ALPHABETA_H
