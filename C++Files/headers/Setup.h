//
// Created by themagicalplace on 3/19/20.
//
#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <vector>
#include "ChessPieces.h"
#ifndef PROJ1_SETUP_H
#define PROJ1_SETUP_H

void piece_string_conversion(std::string& pos);
class Setup {
public:
    std::string path;
    std::ifstream stream;
    std::map<std::string,ChessPieces::Piece *> board;
    Setup();

};

ChessPieces::Piece* get_piece(std::string piece, std::string position, std::string owner);

#endif //PROJ1_SETUP_H
