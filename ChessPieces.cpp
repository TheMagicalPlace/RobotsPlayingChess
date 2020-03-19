//
// Created by 17344 on 3/19/2020.
//

#include "ChessPieces.h"

ChessPieces::Piece::Piece(std::string owner) :owner(std::move(owner)) {
    rng_val = get_rng_val();
}

int ChessPieces::Piece::get_rng_val() {
    srand(time(nullptr));
    return rand();
}

std::vector<std::string> ChessPieces::Piece::move_range(std::map<std::string, Piece> current_state, bool is_king_check) {

    // Setting up individual directions to check in
    std::string up_right{position}; std::string up_left{position}; std::string down_right{position}; std::string down_left{position};
    std::string up{position}; std::string down{position}; std::string left{position}; std::string right{position};
    if(piece == "Twr")
    {
        up_right = std::to_string(-1);up_left = std::to_string(-1);down_right = std::to_string(-1); down_left = std::to_string(-1);
    }
    else if(piece == "Bsp")
    {
        up = std::to_string(-1);left= std::to_string(-1);down = std::to_string(-1); right = std::to_string(-1);
    }
    std::vector<std::string> moves{};
    for(int i{1};i < 8;++i)
    {
        if(up_left =="-1" && up_right == "-1" && down_left== "-1" && down_right== "-1" && up== "-1" &&down== "-1" &&left== "-1" &&right== "-1" )
        {
            break;
        }
        if (up_right != "-1")
        {
            std::string up_right{""};
            char a = (int) position[0]+1;
            char b = (int) position[1]+1;
            up_right.push_back(a);up_right.push_back(b);
            std::cout << a << b << up_right;
        }

    }
    return std::vector<std::string>();
}

std::vector<std::string> ChessPieces::Pawn::move_range(std::map<std::string, Piece> current_state, bool is_king_check) {
    return Piece::move_range(current_state, is_king_check);
}



void ChessPieces::Piece::update_positions(std::map<std::string, Piece> current_state) {

}





std::vector<std::string>
ChessPieces::Knight::move_range(std::map<std::string, Piece> current_state, bool is_king_check) {
    return Piece::move_range(current_state, is_king_check);
}

std::vector<std::string> ChessPieces::King::move_range(std::map<std::string, Piece> current_state, bool is_king_check) {
    return Piece::move_range(current_state, is_king_check);
}
