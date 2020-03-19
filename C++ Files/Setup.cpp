//
// Created by themagicalplace on 3/19/20.
//

#include "Setup.h"
#include "ChessPieces.h"
#include <printf.h>
using namespace std;

Setup::Setup() {
    ifstream file1;
    file1.open("/home/themagicalplace/CLionProjects/RobotsPlayingChess/text1.txt");

    while (!file1.eof()) {
        string pos;
        string piece;
        string owner;
        cout << piece << " " << pos << " " << owner << endl;
        file1 >> pos;file1 >> piece; file1 >> owner;
        ChessPieces::Piece* pce {get_piece(piece,owner)};
        board.insert(pair<string,ChessPieces::Piece*>(pos,pce));


    }
    for(const auto& elem :  board)
    {
        auto h = *elem.second;
        std::cout << elem.first << " " << " " << h.get_piece() <<" " <<h.owner << "\n";
    }



}

ChessPieces::Piece * get_piece(string& piece,string& owner)
{
    cout << piece << " ";
    if (piece == "Knt")

    {
        return new ChessPieces::Knight(owner);
    }
    else if (piece == "Twr")
    {
        return new ChessPieces::Rook(owner);
    }
    else if (piece == "Qun")
    {
        return new ChessPieces::Queen(owner);
    }
    else if (piece == "Kng")
    {
        return new ChessPieces::King(owner);
    }
    else if (piece == "Bsp")
    {
        return new ChessPieces::Bishop(owner);
    }
    else if (piece == "Pwn")
    {
        return new ChessPieces::Pawn(owner);
    }
    else
    {
        return new ChessPieces::Piece("None");
    }


}

