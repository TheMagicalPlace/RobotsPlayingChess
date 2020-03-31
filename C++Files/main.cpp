
#include "Python.h"
#include <iostream>
#include <algorithm>
#include <fstream>
#include "headers/ChessPieces.h"
#include "headers/Setup.h"
#include "headers/alphabeta.h"

using namespace std;
void test1();

void TestsA(std::map<std::string,std::shared_ptr<ChessPieces::Piece>> const &board);
double TestsB(std::map<std::string,std::shared_ptr<ChessPieces::Piece>> setup);


int main() {
    string hold{};
    string t{};
    string line = { " " };
    ifstream file1;
    file1.open("/home/themagicalplace/CLionProjects/RobotsPlayingChess/text1.txt");
    while(!file1.eof())
    {

        file1>>hold;
        t.append(hold);
        t.append(" ");
        hold.clear();
    }

    auto board = setup(t);
    std::map<std::string,std::shared_ptr<ChessPieces::Piece>> i;i.insert(board.begin(),board.end());
    TestsA(std::move(board));
    TestsB(i);
    return 0;
};


void TestsA(std::map<std::string,std::shared_ptr<ChessPieces::Piece>>const & board)
{
    auto pce3 = std::make_shared<ChessPieces::Piece>("White","4a","Qun");
    auto a3 = pce3;
    a3->move_range(board,false );
    cout<<endl<<endl;

    auto pce2 = std::make_shared<ChessPieces::Piece>("White","4a","Bsp");
    auto a2 = pce2;
    a2->move_range(board,false );
    cout<<endl;



    auto pce4 = std::make_shared<ChessPieces::Piece>("White","4a","Kng");
    auto a4 = pce4;
    a4->move_range(board,false );
    cout<<endl<<endl;
    std::map<std::string,std::shared_ptr<ChessPieces::Piece>> c;
    c.insert(board.begin(),board.end());
    auto pce = std::make_shared<ChessPieces::Piece>("White","4a","Twr");
    c.at("1a") = pce;

    a4->move_range(board,false );
    cout<<endl;
}

double TestsB(std::map<std::string,std::shared_ptr<ChessPieces::Piece>> setup)
{
    double result;
    for(int i{2};i<8;++i) {
        std::time_t init = std::time(nullptr);
        AlphaBeta alphabeta_test{"White", setup, int{i}, true};
        //delete &alphabeta_test;
        result = alphabeta_test.call(true);
        //delete &alphabeta_test;
        cout << "Depth : " << i << " Run Time : " << init - std::time(nullptr) << endl;
        cout << "Final Size of AB object : " << sizeof(alphabeta_test) << " Result : " << result << endl << endl;
    }
    return result;

}

void TestSizes(){
    std::cout<<"Size of 'double' :"<<sizeof(double)<<endl;
    std::cout<<"Size of 'Piece' :"<<sizeof(Piece)<<endl;
    std::cout<<"Size of 'Chess Node' :"<<sizeof(ChessNode)<<endl;
    std::cout<<"Size of 'AB object' :"<<sizeof(AlphaBeta)<<endl;
    std::cout<<"Size of '*Piece' :"<<sizeof(std::shared_ptr<Piece>)<<endl;
    std::cout<<"Size of 'instanced Piece' :"<<sizeof(ChessPieces::Piece("White","4a","Bsp"))<<endl;
    std::cout<<"Size of '*Piece' :"<<sizeof(std::shared_ptr<Piece>)<<endl;
    std::cout<<"Size of 'map' :"<<sizeof(std::map<string,std::shared_ptr<ChessPieces::Piece>>)<<endl;

};