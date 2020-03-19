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
#include "ChessPieces.h"
#ifndef PROJ1_CHESSBOARD_H
#define PROJ1_CHESSBOARD_H
namespace Chessboard{
    using namespace std;
    class ChessBoard {
    public:
        map<string,ChessPieces::Piece> current_state;
        ChessBoard();
    private:
        void setup();

    };


    #endif //PROJ1_CHESSBOARD_H
}