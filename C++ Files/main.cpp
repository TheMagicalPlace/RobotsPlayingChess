#define PY_SSIZE_T_CLEAN
#include "/usr/include/python3.7/Python.h"
#include <iostream>
#include <algorithm>
#include <fstream>
#include "ChessPieces.h"
#include "Setup.h"
using namespace std;
void test1();

int main() {


    string line = { " " };
    ifstream file1;
    file1.open("/home/themagicalplace/CLionProjects/RobotsPlayingChess/text1.txt");

    Setup s {};
    auto pce = new ChessPieces::Piece("White","a4","Twr");
    s.board["a4"] = pce;

    auto a = pce;
    a->move_range(s.board,false );

    return 0;
};


