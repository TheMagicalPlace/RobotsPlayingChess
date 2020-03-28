//
// Created by themagicalplace on 3/28/20.
//

#ifndef ROBOTSPLAYINGCHESS_CPPPYTHONCROSSMODULE_H
#define ROBOTSPLAYINGCHESS_CPPPYTHONCROSSMODULE_H

#include <iostream>
#include <string>
#include <vector>
#include "alphabeta.h"
#include "Setup.h"
#include "alphabeta.h"
#include "ChessPieces.h"


double PythonCPPRunAlphabeta(std::string boardstring,int depth, std::string player);

#endif //ROBOTSPLAYINGCHESS_CPPPYTHONCROSSMODULE_H
