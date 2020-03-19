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
        std::vector<std::string> move_range(std::map<std::string, Piece *> current_state, bool is_king_check);
        void update_positions(std::map<std::string, Piece> current_state);
        int get_rng_val();
        std::string get_piece(){ return piece;}

    private:
        std::string piece {"na"};
        int rng_val = get_rng_val();
        static constexpr int value{0};

    };


    class Pawn: public Piece{
    public:

        explicit Pawn(std::string owner);

        std::vector<std::string> move_range(std::map<std::string, Piece *> current_state, bool is_king_check);
    private:
        static constexpr int value{1};
        std::string piece;
    };

    class Rook: public Piece{
    public:
        explicit Rook(std::string owner);

    private:
        const std::string piece;
        static constexpr int value{5};

    };

    class Bishop: public Piece{
    public:
        explicit Bishop(std::string owner);
        const std::string piece{"Bsp"};
    private:
        static constexpr int value{3};

    };

    class Queen: public Piece{
    public:
        explicit Queen(std::string owner);
        const std::string piece{"Qun"};
    private:
        static constexpr int value{8};

    };

    class Knight: public Piece{
    public:
        explicit Knight(std::string owner);
        std::vector<std::string> move_range(std::map<std::string, Piece *> current_state, bool is_king_check);
        const std::string piece{"Twr"};
    private:
        static constexpr int value{5};

    };

    class King: public Piece{
    public:
        explicit King(std::string owner);
        std::vector<std::string> move_range(std::map<std::string, Piece *> current_state, bool is_king_check);
        bool is_in_check{false};
        std::vector<std::string> king_check;
        const std::string piece{"Kng"};

    private:
        static constexpr int value{1000000};

    };

}
#endif //PROJ1_CHESSPIECES_H
