//
// Created by 17344 on 3/19/2020.
//

#include <cstdio>
#include <cstdlib>
#include <string>
#include <random>
#include <iostream>
#include <iomanip>
#include <string>
#include <map>
#include <random>
#include <cmath>
#include <ctime>
#include <memory>

#ifndef PROJ1_CHESSPIECES_H
#define PROJ1_CHESSPIECES_H


namespace ChessPieces {

    // sets the default value for the piece value map for blank spaces/non-pieces



    class Piece {

    public:
        static const std::map<std::string, int> piece_values;
        const std::map<std::string,std::string> opponent {{"Black","White"},{"White","Black"},{"None","None"}};
        const std::string owner;
        std::string position;
        const std::string piece;
        const int value = ChessPieces::Piece::piece_values.at(piece);

        Piece(std::string owner, std::string piece, std::string position)
        :owner(owner),piece(piece),position(position){};

        std::vector<std::string> move_range(std::map<std::string, std::shared_ptr<Piece>> const & board, bool is_king_check);
        std::vector<std::string> move_range_pawn(std::map<std::string, std::shared_ptr<Piece>> const & current_state, bool is_king_check);
        std::vector<std::string> move_range_knight(std::map<std::string, std::shared_ptr<Piece>> const & current_state, bool is_king_check);
        std::string get_position(std::map<std::string,std::shared_ptr<Piece>> const & current_state);

    private:
        std::vector<std::string> moves{};
    };

}

#endif //PROJ1_CHESSPIECES_H
