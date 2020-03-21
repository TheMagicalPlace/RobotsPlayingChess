//
// Created by 17344 on 3/19/2020.
//




#include <algorithm>
#include <utility>
#include "../headers/ChessPieces.h"

// Parent 'Piece' Methods

using  string = std::string ;

ChessPieces::Piece::Piece(std::string owner,std::string position,std::string piece)
    :owner(owner),piece(piece),position(position) {
    rng_val = get_rng_val();
    value = ChessPieces::pieces.piece_values[piece];
}

int ChessPieces::Piece::get_rng_val() {
    srand(time(nullptr));
    return rand();
}

std::vector<std::string> ChessPieces::Piece::move_range(std::map<std::string, Piece *>& current_state, bool is_king_check) {
    if (piece == "Pwn"){
        return move_range_pawn(current_state,is_king_check);
    }
    else if (piece=="Knt")
    {
        return move_range_knight(current_state,is_king_check);
    }
    const std::string letters{"abcdefghABCDEFGH"};
    const std::string numbers{"12345678"};
    moves.clear();      // clears out move vector upon new move search;

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
            char b =  position[1];
            up[0] = a;
            up[1] = b;

        }
        if (down != "-1") {
            char a = (int) position[0] - i;
            char b =  position[1];
            down[0] =a;
            down[1] = b;

        }
        if (left != "-1") {
            char a =  position[0];
            char b = (int) position[1] - i;
            left[0] = a;
            left[1] = b;

        }
        if (right != "-1") {
            char a;
            a =  position[0];
            char b;
            b = (int) position[1] + i;
            right[0] = a;
            right[1] = b;
        }

        // setting up intermediate holding vectors
        std::vector<std::string *> next {&up,&down,&left,&right,&up_left,&up_right,&down_left,&down_right};
        std::vector<std::string> pots{};
        std::vector<std::string> potsR{};

        // Removing invalid moves
        for (auto nxt : next)

        {
            string nxt_val = *nxt;
            //std::cout <<nxt_val << " ";
            if(std::count(numbers.begin(),numbers.end(),nxt_val[0]) == 1 && std::count(letters.begin(),letters.end(),nxt_val[1]) == 1)
            {
                pots.push_back(nxt_val);
            }
        }
        //std::cout <<std::endl;

        // Can't move onto friendly spaces (except during king check)
        for  (auto &pot : pots)
        {


            if (current_state[pot]->get_owner() != owner || is_king_check)
            {
                potsR.push_back(pot);
                //std::cout << current_state[pot]->get_owner()<< " " << owner << " " <<pot<<  "| ";
                //std::cout << pot << " ";
            }
        }

        std::vector<std::string> tr {};
        for  (auto &pot : potsR)
        {
            if(is_king_check)
            // accounts for opposing pieces as an avalible move & blocker
            {
                if (current_state[pot][0].owner == opponent[owner])
                {
                    if (current_state[pot][0].get_piece() == "Kng" && current_state[pot][0].owner != owner)
                    {
                        moves.push_back(pot);
                    }
                    else
                    {
                        moves.push_back(pot);
                        tr.push_back(pot);
                    }

                }
                else if (current_state[pot][0].owner == owner)
                {
                    tr.push_back(pot);
                    moves.push_back(pot);
                }
                else
                {
                moves.push_back(pot);
                }

            }
            else
            {
                if (current_state[pot][0].owner == opponent[owner])
                {
                    moves.push_back(pot);
                    tr.push_back(pot);
                }
                else
                {
                    moves.push_back(pot);
                }
            }
        }

        // Kings can only move one space
        if(this->get_piece() == "Kng")
            break;

        // removing relevant nodes from consideration
        sort(tr.begin(), tr.end());



        // removing spaces that allow no further movement past it


        for(auto & r : potsR)
        {
            if (std::count(tr.begin(), tr.end(), r))
            {
                r = "-1";
            }
        }


        // assigning
        for(int i{0};i<next.size();++i)
        {
            if (is_king_check)
            {
                if (not std::count(potsR.begin(),potsR.end(),*next[i]) || current_state[*next[i]][0].owner == owner)
                {
                    *next[i] = "-1";
                }

            }
            else
            {
                if (not std::count(potsR.begin(),potsR.end(),*next[i]))
                {
                    *next[i] = "-1";
                }
            }
        }

        //checking that next values are correct
        //for(auto &a : next)
        //{
        //    std::cout << *a << " ";
        //}
        //std::cout <<std::endl;


    }
    std::sort(moves.begin(),moves.end());
    std::cout <<std::endl<<"Piece : "<<this->piece<<std::endl<<"Moves : ";
    for(auto &a : moves)
    {
        std::cout << a << " ";
    }

    return std::vector<std::string>();
}

std::vector<std::string> ChessPieces::Piece::move_range_pawn(std::map<std::string, Piece *>& current_state, bool is_king_check)
{
    if(owner=="Black")
    {

    }
}

std::vector<std::string> ChessPieces::Piece::move_range_knight(std::map<std::string, Piece *>& current_state, bool is_king_check){}

void ChessPieces::Piece::update_positions(std::map<std::string, Piece> current_state) {
    rng_val = get_rng_val();
}

std::string ChessPieces::Piece::get_position(std::map<std::string, Piece *> &current_state) {
    for (auto &space :current_state)
    {
        if (space.second == this)
            return space.first;
    }
    return "not found";
}

