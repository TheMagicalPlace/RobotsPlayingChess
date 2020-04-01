//
// Created by themagicalplace on 3/19/20.
//

#include "../headers/Setup.h"





using string = std::string;


std::map<std::string,std::shared_ptr<ChessPieces::Piece>> setup(std::string &boards) {
    std::map<std::string,std::shared_ptr<ChessPieces::Piece>> board{};
    std::istringstream boardstream {boards};



    while (!boardstream.eof()) {
        string pos;
        string piece;
        string owner;

        boardstream >> pos;boardstream >> piece; boardstream >> owner;
        if(pos.empty() || piece.empty() || owner.empty())
            break;
        //std::cout<<pos<< "-"<<piece<<"-"<<owner<<"|";
        piece_string_conversion(pos);
        std::shared_ptr<ChessPieces::Piece> pce = std::make_shared<ChessPieces::Piece>(owner,pos,piece);
        board.insert(std::pair<string,std::shared_ptr<ChessPieces::Piece>>(pos,pce));


    }
    auto a = *board.begin()->second;
    //std::cout<<"first "<<a.position;

    //for(const auto& elem :  board)
    //{
    //    auto h = *elem.second;
    //    std::cout << elem.first  << " " << h.position <<" " <<h.owner << "\n";
    //}

    return board;



}


void piece_string_conversion(string& pos)
{
    //cout<<"input : "<<pos;
    switch(pos[0])
    {
        case 'a' : pos[0] = '1';break;
        case 'b' : pos[0] = '2';break;
        case 'c' : pos[0] = '3';break;
        case 'd' : pos[0] = '4';break;
        case 'e' : pos[0] = '5';break;
        case 'f' : pos[0] = '6';break;
        case 'g' : pos[0] = '7';break;
        case 'h' : pos[0] = '8';break;
    }
    switch(pos[1])
    {
        case '1' : pos[1] = 'a';break;
        case '2' : pos[1] = 'b';break;
        case '3' : pos[1] = 'c';break;
        case '4' : pos[1] = 'd';break;
        case '5' : pos[1] = 'e';break;
        case '6' : pos[1] = 'f';break;
        case '7' : pos[1] = 'g';break;
        case '8' : pos[1] = 'h';break;
    }
    //cout<<" output : "<<pos<<" "<<endl;
}


