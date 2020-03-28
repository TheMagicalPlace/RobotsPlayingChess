//
// Created by themagicalplace on 3/28/20.
//

#include "CppPythonCrossModule.h"


double PythonCPPRunAlphabeta(std::string boardstring,int depth, std::string player)
{
    // Getting Board
    auto board = setup(boardstring);
    AlphaBeta alphabeta_test{player, board, int{depth}, true};
    double result = alphabeta_test.call(true);
    return result;

}