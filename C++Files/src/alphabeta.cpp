//
// Created by themagicalplace on 3/20/20.
//

#include "../headers/alphabeta.h"
#include <utility>
#include <vector>
#include <iostream>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iterator>



std::shared_ptr<ChessNode> ChessNode::spawn_child(std::shared_ptr<Piece> const &piece, string move) {
    auto nboard{this->board};

    // debugging invalid piece positions
    //if (piece->position.length() > 2)
    //    std::cout << piece->position;

    // get old piece position and reassign to new blank for child board and move piece to new position
    string old = piece->position;
    nboard[move] = piece;
    nboard[old] = std::make_shared<Piece>("None",old,"na");

    // create new node & assign pointer
    auto new_node= std::make_shared<ChessNode>(this->depth - 1, nboard);

    childs.push_back(new_node);
    return new_node;
}


std::shared_ptr<Piece> ChessNode::next_piece() {


    if (index<64)
    {

        auto pce = board_iter[index];       // get the piece - smart pointer to piece
        ++index;                            // and increase the index
        return pce;

    }
    else
    {
        return exit_piece;
                                // return null if exhausted
    }


}

std::vector<std::shared_ptr<ChessNode>> AlphaBeta::child_node_finder(std::shared_ptr<ChessNode> const &node, int depth, bool is_maxing) const {

    // container for found children
    std::vector<std::shared_ptr<ChessNode>> next_nodes{} ;

    // determines which players pieces moves are examined
    string current_player;
    if (is_maxing)
        current_player = player;
    else
        current_player = opponent.at(player);


    // Implemented to be semi-analogous to a python generator, what this does is create the child nodes for each
    // piece at a time, therefore if the main alpha-beta search breaks early no time will have been wasted in
    // generating extraneous child nodes for the other pieces.

    std::shared_ptr<Piece> piece = node->next_piece();

    //std::cout<<&piece;
    while (piece->owner != "EXIT")
    {
        //std::cout<<" t "<<piece.get_piece();

        if (piece->owner == current_player)
        {
            std::vector<std::string> moves = piece->move_range(node->board, false);
            if (moves.empty()) {
                //std::cout<<piece.position<<" is empty, moving to next";
                piece = node->next_piece();
            }
            else
            {
                for (string &move : moves)
                {
                    next_nodes.push_back(node->spawn_child(piece, move));
                }
                return next_nodes;
            }
        }
        else
            piece = node->next_piece();
    }

    // returns the empty vector
    return next_nodes;
}

double AlphaBeta::node_evaluation_heuristic(std::shared_ptr<ChessNode> const &node,bool is_maxing)
{
    double value{0};
    string current_player;
    if (is_maxing)
        current_player = player;
    else
        current_player = opponent.at(player);

    std::shared_ptr<Piece> next = node->next_piece();
    while (next->owner != "EXIT")
    {
        
            if (next->owner == current_player)
            {
                value += next->value;
            }
            else if (next->owner == next->opponent.at(current_player))
            {
            value -= next->value;
            }
        next = node->next_piece();
    }

    return value;
}

double AlphaBeta::ab_search(std::shared_ptr<ChessNode> const &node, int depth, bool maxing_player, int alpha, int beta) {

    // for debugging odd scores or exits
    if (depth > (int)search_depth/2)
    {
        for(int i{depth};i<search_depth;++i)
            std::cout<<"  ";
        std::cout<< "Entering Depth : "<<depth<<std::endl;
    }


    double value;

    // at maximum depth score board and assign value to node
    if (depth == 0)
        value = node_evaluation_heuristic(node,maxing_player);
    else if (maxing_player)
    {
        auto nodes = child_node_finder(node,depth,maxing_player);
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
            }

            // breaks out of the loop early on condition
            if (alpha >=beta)
                nodes.clear();
            else
                nodes= child_node_finder(node,depth,maxing_player);

        }
    }
    else
    {
        auto nodes = child_node_finder(node,depth,maxing_player);
        value =100000;
        while(not nodes.empty()) {
            for (auto &n : nodes) {
                double val = ab_search(n, depth - 1, true, alpha, beta);
                value = std::fmin(val, value);
                beta = std::fmin(beta, value);
            }

            // breaks out of the loop early on condition
            if (alpha >= beta)
                nodes.clear();
            else
                nodes = child_node_finder(node, depth, maxing_player);
        }
    }

    // for debugging odd scores or exits
    if (depth > 1)
    {
        for(int i{depth};i<search_depth;++i)
            std::cout<<"  ";
        std::cout<< "Exiting Depth : "<<depth<<" Score : "<<value<<" Alpha : "<<alpha<<" Beta : "<<beta<<std::endl;
    }

    //  set node value & return
    node->set_value(value);
    return value;
}

double AlphaBeta::call(bool maxing_player) {
    std::cout<<"initializing call";
    double result = ab_search(root_node,search_depth,maxing_player,-100000,100000);
    return result;
}
