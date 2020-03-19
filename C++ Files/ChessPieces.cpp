//
// Created by 17344 on 3/19/2020.
//




#include <algorithm>
#include <utility>
#include "ChessPieces.h"

// Parent 'Piece' Methods

ChessPieces::Piece::Piece(std::string owner) :owner(std::move(owner)) {
    rng_val = get_rng_val();
}

int ChessPieces::Piece::get_rng_val() {
    srand(time(nullptr));
    return rand();
}

std::vector<std::string> ChessPieces::Piece::move_range(std::map<std::string, Piece *> current_state, bool is_king_check) {
    const std::string letters{"abcdefghABCDEFGH"};
    const std::string numbers{"12345678"};


    // Setting up individual directions to check in
    std::string up_right{position};
    std::string up_left{position};
    std::string down_right{position};
    std::string down_left{position};
    std::string up{position};
    std::string down{position};
    std::string left{position};
    std::string right{position};
    if (piece == "Twr") {
        up_right = std::to_string(-1);
        up_left = std::to_string(-1);
        down_right = std::to_string(-1);
        down_left = std::to_string(-1);
    } else if (piece == "Bsp") {
        up = std::to_string(-1);
        left = std::to_string(-1);
        down = std::to_string(-1);
        right = std::to_string(-1);
    }
    std::vector<std::string> moves{};
    for (int i{1}; i < 9; ++i) {
        if (up_left == "-1" && up_right == "-1" && down_left == "-1" && down_right == "-1" && up == "-1" &&
            down == "-1" && left == "-1" && right == "-1") {
            break;
        }
        // updating each potential move, I'm sure there's a more concise way to do this
        if (up_right != "-1") {
            char a = (int) position[0] + i;
            char b = (int) position[1] + i;
            up_right[0] = a;
            up_right[1] = b;
        }
        if (up_left != "-1") {
            char a = (int) position[0] + i;
            char b = (int) position[1] - i;
            up_left[0] = a;
            up_left[1] = b;
        }
        if (down_right != "-1") {
            char a = (int) position[0] - i;
            char b = (int) position[1] + i;
            down_right[0] = a;
            down_right[1] = b;
        }
        if (down_left != "-1") {
            char a = (int) position[0] - i;
            char b = (int) position[1] - i;
            down_left[0] = a;
            down_left[1] = b;;

        }
        if (up != "-1") {
            char a = (int) position[0] + i;
            char b = (int) position[1];
            up[0] = a;
            up[1] = b;

        }
        if (down != "-1") {
            char a = (int) position[0] - i;
            char b = (int) position[1];
            down[0] = a;
            down[1] = b;

        }
        if (left != "-1") {
            char a = (int) position[0];
            char b = (int) position[1] - i;
            left[0] = a;
            left[1] = b;

        }
        if (right != "-1") {
            char a = (int) position[0];
            char b = (int) position[1] - i;
            right[0] = a;
            right[1] = b;
        }

        // setting up intermediate holding vectors
        std::vector<std::string> next {up,down,left,right,up_left,up_right,down_left,down_right};
        std::vector<std::string> pots{};
        std::vector<std::string> potsR{};

        // Removing invalid moves
        for (auto &nxt : next)
        {

            if(std::count(numbers.begin(),numbers.end(),nxt[0]) == 1 && std::count(letters.begin(),letters.end(),nxt[1]) == 1)
            {
                pots.push_back(nxt);
            }
        }

        // Can't move onto friendly spaces
        for  (auto &pot : pots)
        {
            if (pot != owner)
            {
                potsR.push_back(pot);
                std::cout << pot << " ";
            }
        }

    }
    return std::vector<std::string>();
}

void ChessPieces::Piece::update_positions(std::map<std::string, Piece> current_state) {
    rng_val = get_rng_val();
}

// Pawn Methods
ChessPieces::Pawn::Pawn(std::string owner) : Piece(std::move(owner)) , piece("Pwn") {}

std::vector<std::string> ChessPieces::Pawn::move_range(std::map<std::string, Piece *> current_state, bool is_king_check) {
    return Piece::move_range(current_state, is_king_check);
}



// Knight Methods

ChessPieces::Knight::Knight(std::string owner) : Piece(std::move(owner)),piece("Knt") {

}

std::vector<std::string>
ChessPieces::Knight::move_range(std::map<std::string, Piece *> current_state, bool is_king_check) {
    return Piece::move_range(std::move(current_state), is_king_check);
}


// King Methods
ChessPieces::King::King(std::string owner) : Piece(std::move(owner)) ,piece("Kng"){

}

std::vector<std::string> ChessPieces::King::move_range(std::map<std::string, Piece *> current_state, bool is_king_check) {
    return Piece::move_range(std::move(current_state), is_king_check);
}



// Rook Methods
ChessPieces::Rook::Rook(std::string owner) : Piece(std::move(owner)) , piece("Twr"){

}


// Bishop Methods

ChessPieces::Bishop::Bishop(std::string owner) : Piece(std::move(owner)),piece("Bsp") {

}

// Queen Methods

ChessPieces::Queen::Queen(std::string owner) : Piece(std::move(owner)),piece("Qun") {

}
