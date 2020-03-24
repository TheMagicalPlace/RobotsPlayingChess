#define PY_SSIZE_T_CLEAN
#include "/usr/include/python3.7/Python.h"
#include <iostream>
#include <algorithm>
#include <fstream>
#include "headers/ChessPieces.h"
#include "headers/Setup.h"
#include "headers/alphabeta.h"

using namespace std;
void test1();

void TestsA(Setup& s);
double TestsB(Setup& setup);


int main() {


    string line = { " " };
    ifstream file1;
    file1.open("/home/themagicalplace/CLionProjects/RobotsPlayingChess/text1.txt");

    Setup s {};
    double d {TestsB(s)};
    return 0;
};


void TestsA(Setup& s)
{
    auto pce3 = std::make_shared<ChessPieces::Piece>("White","4a","Qun");
    auto a3 = pce3;
    a3->move_range(s.board,false );
    cout<<endl<<endl;

    auto pce2 = std::make_shared<ChessPieces::Piece>("White","4a","Bsp");
    auto a2 = pce2;
    a2->move_range(s.board,false );
    cout<<endl;



    auto pce4 = std::make_shared<ChessPieces::Piece>("White","4a","Kng");
    auto a4 = pce4;
    a4->move_range(s.board,false );
    cout<<endl<<endl;

    auto pce = std::make_shared<ChessPieces::Piece>("White","4a","Twr");
    s.board["1a"] = pce;
    auto a = pce;
    a->move_range(s.board,false );
    cout<<endl;
}

double TestsB(Setup& setup)
{

 AlphaBeta alphabeta_test{"White",setup.board,int{6},true};
 double result = alphabeta_test.call(true);
 return result;

}