//
// Created by themagicalplace on 3/19/20.
//

#include <memory>
#include <utility>
#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <vector>
#include <memory>
#include <ios>
#include <iso646.h>
#include "ChessPieces.h"
#include <sstream>
#ifndef PROJ1_SETUP_H
#define PROJ1_SETUP_H

std::map<std::string,std::shared_ptr<ChessPieces::Piece>> setup(std::string &boards);
void piece_string_conversion(std::string& pos);
std::shared_ptr<ChessPieces::Piece> get_piece(std::string piece, std::string position, std::string owner);

#endif //PROJ1_SETUP_H
