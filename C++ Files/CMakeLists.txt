cmake_minimum_required(VERSION 3.15)
project(RobotsPlayingChess)

set(CMAKE_CXX_STANDARD 14)

add_executable(RobotsPlayingChess main.cpp "src/ChessPieces.cpp" "headers/ChessPieces.h" "src/ChessBoard.cpp" "headers/ChessBoard.h" src/Setup.cpp headers/Setup.h src/alphabeta.cpp headers/alphabeta.h)