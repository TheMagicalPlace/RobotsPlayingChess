//
// Created by themagicalplace on 3/19/20.
//

#include "../headers/Setup.h"
#include "../headers/ChessPieces.h"
#include <printf.h>
using namespace std;

ChessPieces::Piece * get_piece(string piece,string position,string owner)
{
    cout << piece << " ";
    return new ChessPieces::Piece(owner,piece,position);


}

Setup::Setup() {
    ifstream file1;
    file1.open("/home/themagicalplace/CLionProjects/RobotsPlayingChess/text1.txt");

    while (!file1.eof()) {
        string pos;
        string piece;
        string owner;
        cout << piece << " " << pos << " " << owner << endl;
        file1 >> pos;file1 >> piece; file1 >> owner;
        ChessPieces::Piece* pce {get_piece(piece, pos, owner)};
        board.insert(pair<string,ChessPieces::Piece*>(pos,pce));


    }
    for(const auto& elem :  board)
    {
        auto h = *elem.second;
        std::cout << elem.first << " " << " " << h.position <<" " <<h.owner << "\n";
    }



}



