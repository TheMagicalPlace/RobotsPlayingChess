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
    ChessPieces::Piece ppp = ChessPieces::Piece("White");
    ChessPieces::Piece pep = ChessPieces::Piece("Black");
    string a{""};

    string line = { " " };
    ifstream file1;
    file1.open("/home/themagicalplace/CLionProjects/RobotsPlayingChess/text1.txt");

    Setup s {};
};


void test1() {
    std::string letters{"abcdefghABCDEFGH"};
    std::string numbers{"12345678"};
    std::string position{"1A"};
    std::string piece{"Kng"};
    std::vector<std::string> _ ;
    std::string owner{"Black"};
    std::map<std::string , std::string > current_state;
    for(char &l : letters)
    {
        for (char &n : numbers)
        {
            std::string nstr{""};
            nstr.push_back(n);nstr.push_back(l);
            std::cout << nstr;
            current_state.insert(std::pair<std::string,std::string>(nstr,"White"));

        }
    }



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
    for(int i{1};i < 9;++i)
    {
        if(up_left =="-1" && up_right == "-1" && down_left== "-1" && down_right== "-1" && up== "-1" &&down== "-1" &&left== "-1" &&right== "-1" )
        {
            break;
        }
        if (up_right != "-1")
        {
            char a = (int) position[0]+i;
            char b = (int) position[1]+i;
            up_right[0]=a;up_right[1]=b;
        }
        if (up_left != "-1")
        {
            char a = (int) position[0]+i;
            char b = (int) position[1]-i;
            up_left[0]=a;up_left[1]=b;
        }
        if (down_right != "-1")
        {
            char a = (int) position[0]-i;
            char b = (int) position[1]+i;
            down_right[0]=a;down_right[1]=b;
        }
        if (down_left != "-1")
        {
            char a = (int) position[0]-i;
            char b = (int) position[1]-i;
            down_left[0]=a;down_left[1]=b;;

        }
        if (up != "-1")
        {
            char a = (int) position[0]+i;
            char b = (int) position[1];
            up[0]=a;up[1]=b;

        }
        if (down != "-1")
        {
            char a = (int) position[0]-i;
            char b = (int) position[1];
            down[0]=a;down[1]=b;

        }
        if (left != "-1")
        {
            char a = (int) position[0];
            char b = (int) position[1]-i;
            left[0]=a;left[1]=b;

        }
        if (right != "-1")
        {
            char a = (int) position[0];
            char b = (int) position[1]-i;
            right[0]=a;right[1]=b;


        }


        std::vector<std::string> next {up,down,left,right,up_left,up_right,down_left,down_right};
        std::vector<std::string> pots{};
        std::vector<std::string> potsR{};
        for (auto &nxt : next)
        {

            if(std::count(numbers.begin(),numbers.end(),nxt[0]) == 1 && std::count(letters.begin(),letters.end(),nxt[1]) == 1)
            {
                pots.push_back(nxt);
            }
        }
        for  (auto &pot : pots)
        {
            if (current_state[pot] != owner)
            {
                potsR.push_back(pot);
                std::cout << pot << " ";
            }
        }
        for (auto &potX : potsR)
        {
            ;
        }

    }


}