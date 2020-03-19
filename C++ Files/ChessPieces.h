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

#ifndef PROJ1_CHESSPIECES_H
#define PROJ1_CHESSPIECES_H


namespace ChessPieces {

    class Piece {

    public:
        std::map<std::string,std::string> opponent {{"Black","White"},{"White","Black"}};
        std::string owner;
        std::string position;
        std::vector<std::string> moves{};

        Piece(std::string owner, std::string position, std::string piece);

        int show_rng_value() { return rng_val; };

        std::vector<std::string> move_range(std::map<std::string, Piece *>& current_state, bool is_king_check);
        std::vector<std::string> move_range_pawn(std::map<std::string, Piece *>& current_state, bool is_king_check);
        std::vector<std::string> move_range_knight(std::map<std::string, Piece *>& current_state, bool is_king_check);
        void update_positions(std::map<std::string, Piece> current_state);

        std::string get_owner(){ return owner;}
        int get_rng_val();

        std::string get_piece() { return piece; }

    private:
        std::string piece;
        int rng_val = get_rng_val();
        static constexpr int value{0};

    };

}

#endif //PROJ1_CHESSPIECES_H
