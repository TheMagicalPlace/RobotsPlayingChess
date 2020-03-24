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
    piece.position;
    // debugging invalid piece positions
    if (piece.position.length() > 2)
        std::cout << piece->position;
    string old = piece->position;
    *nboard[move] = *piece;
    *nboard[old] = Piece("None","NA",old);
    ChessNode *new_node = new ChessNode(this, this->depth + 1, nboard);
    new_node->parent = this;
    childs.push_back(new_node);
    return new_node;
}

void ouch (int signal)
    {
    printf("Caught segfault at address %d\n", signal);
    exit(0);
    };

Piece* ChessNode::next_piece() {

    signal(SIGSEGV,ouch);


    if (index<64)
    {
        ++index;
        Piece * pce = &*board_iter->second;       // get the piece
        board_iter++;// and advance the iterator
        return pce;

    }
    else
    {
        return exit_piece;
                                // return null if exhausted
    }


}

AlphaBeta::AlphaBeta(string player, std::map<string, std::shared_ptr<ChessPieces::Piece>> board, int dpth, bool testing)
:player{std::move(player)},testing{testing},root_node(ChessNode(nullptr ,dpth,board)),search_depth{dpth}{

}

std::vector<ChessNode*> AlphaBeta::child_node_finder(ChessNode node, int depth, bool is_maxing) {

    // container for found children
    std::vector<ChessNode*> next_nodes{} ;

    // determines which players pieces moves are examined
    string current_player;
    if (is_maxing)
        current_player = player;
    else
        current_player = opponent[player];


    // Implemented to be semi-analogous to a python generator, what this does is create the child nodes for each
    // piece at a time, therefore if the main alpha-beta search breaks early no time will have been wasted in
    // generating extraneous child nodes for the other pieces.

    Piece piece = *node.next_piece();

    //std::cout<<&piece;
    while (piece.owner != "EXIT")
    {
        //std::cout<<" t "<<piece.get_piece();
        std::vector<std::string> moves = piece.move_range(node.board,false);
        if (piece.owner == current_player)
            for (string &move : moves)
            {
                piece.get_position(node.board);
                next_nodes.push_back(node.spawn_child(&piece,move));
            }
        if (next_nodes.empty())
        {
            //std::cout<<piece.position<<" is empty, moving to next";
            piece = *node.next_piece();

        } else
            return next_nodes;
    }

    // returns the empty vector
    return next_nodes;
}

double AlphaBeta::node_evaluation_heuristic(ChessNode &node)
{
    double value{0};
    Piece next = *node.next_piece();
    while (next.owner != "EXIT")
    {
        
            if (next.owner == player)
            {
                value += next.get_value();
            }
            else if (next.owner == next.opponent[next.owner])
            {
            value -= next.get_value();
            }
        next = *node.next_piece();
    }

    return value;
}

double AlphaBeta::ab_search(ChessNode *node, int depth, bool maxing_player, int alpha, int beta) {
    double value;
    std::cout<< std::endl<<"depth : " << depth <<std::endl;
    // at maximum depth score board and assign value to node
    if (depth == 0)
    {
        value = node_evaluation_heuristic(*node);
        node->set_value(value);
        return value;
    }
    std::cout<<depth<< " "<<&node;
    std::vector<ChessNode*> nodes = child_node_finder(*node,depth,maxing_player);

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
                    node->set_value(value);
                    return value;
                }
            }

            // getting next nodes to examine
            nodes= child_node_finder(*node, depth, maxing_player);

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
                    node->set_value(value);
                    return value;
                }
            }
            nodes= child_node_finder(*node,depth,maxing_player);
        }
    }

    // If no pruning is done set node value & return
    node->set_value(value);
    return value;
}

double AlphaBeta::call(bool maxing_player) {
    std::cout<<"initializing call";
    double result = ab_search(&root_node,search_depth,maxing_player,-100000,100000);
    return result;
}
