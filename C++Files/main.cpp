#define PY_SSIZE_T_CLEAN
#include "/usr/include/python3.7/Python.h"
#include <iostream>
#include <algorithm>
#include <fstream>
#include "headers/ChessPieces.h"
#include "headers/Setup.h"
using namespace std;
void test1();

int main() {


    string line = { " " };
    ifstream file1;
    file1.open("/home/themagicalplace/CLionProjects/RobotsPlayingChess/text1.txt");

    Setup s {};

    auto pce3 = new ChessPieces::Piece("White","4a","Qun");
    auto a3 = pce3;
    a3->move_range(s.board,false );
    cout<<endl<<endl;

    auto pce2 = new ChessPieces::Piece("White","4a","Bsp");
    auto a2 = pce2;
    a2->move_range(s.board,false );
    cout<<endl;



    auto pce4 = new ChessPieces::Piece("White","4a","Kng");
    auto a4 = pce4;
    a4->move_range(s.board,false );
    cout<<endl<<endl;

    auto pce = new ChessPieces::Piece("White","4a","Twr");
    s.board["1a"] = pce;
    auto a = pce;
    a->move_range(s.board,false );
    cout<<endl;





    return 0;
};


