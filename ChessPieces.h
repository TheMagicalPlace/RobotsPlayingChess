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
        std::string owner;
        std::string position;
        explicit Piece(std::string owner);
        int show_rng_value(){ return rng_val;};
        std::vector<std::string> move_range(std::map<std::string, Piece> current_state, bool is_king_check);
        void update_positions(std::map<std::string, Piece> current_state);

    private:
        int rng_val;
        const std::string piece{"Not a Piece"};
        static constexpr int value{0};
        int get_rng_val();
    };


    class Pawn: public Piece{
    public:
        std::vector<std::string> move_range(std::map<std::string, Piece> current_state, bool is_king_check);
    private:
        static constexpr int value{1};
        const std::string piece{"Pwn"};
    };

    class Rook: public Piece{
    private:
        static constexpr int value{5};
        const std::string piece{"Twr"};
    };

    class Bishop: public Piece{
    private:
        static constexpr int value{3};
        const std::string piece{"Bsp"};
    };

    class Queen: public Piece{
    private:
        static constexpr int value{8};
        const std::string piece{"Qun"};
    };

    class Knight: public Piece{
    public:
        std::vector<std::string> move_range(std::map<std::string, Piece> current_state, bool is_king_check);
    private:
        static constexpr int value{5};
        const std::string piece{"Twr"};
    };

    class King: public Piece{
    public:
        std::vector<std::string> move_range(std::map<std::string, Piece> current_state, bool is_king_check);
        bool is_in_check{false};
        std::vector<std::string> king_check;

    private:
        static constexpr int value{1000000};
        const std::string piece{"Kng"};
    };

}
#endif //PROJ1_CHESSPIECES_H
