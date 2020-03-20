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

    // sets the default value for the piece value map for blank spaces/non-pieces

struct pcs {
    std::map<std::string, int> piece_values
            {
                    {"Kng", 100000},
                    {"Qun", 10},
                    {"Knt", 4},
                    {"Pwn", 1},
                    {"Twr", 4},
                    {"Bsp", 5}
            };
}

static pieces{};


    class Piece {

    public:
        std::map<std::string,std::string> opponent {{"Black","White"},{"White","Black"}};
        std::string owner;
        std::string position;


        Piece(std::string owner, std::string position, std::string piece);

        int show_rng_value() { return rng_val; };

        std::vector<std::string> move_range(std::map<std::string, Piece *>& current_state, bool is_king_check);
        std::vector<std::string> move_range_pawn(std::map<std::string, Piece *>& current_state, bool is_king_check);
        std::vector<std::string> move_range_knight(std::map<std::string, Piece *>& current_state, bool is_king_check);
        void update_positions(std::map<std::string, Piece> current_state);
        std::string get_position(std::map<std::string, Piece *>& current_state);
        std::string get_owner(){ return owner;}
        int get_rng_val();

        std::string get_piece() { return piece; }
        int get_value(){ return value;}

    private:
        std::string piece;
        int rng_val = get_rng_val();
        int value;
        std::vector<std::string> moves{};

    };

}

#endif //PROJ1_CHESSPIECES_H
