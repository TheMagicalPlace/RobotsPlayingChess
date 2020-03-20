cmake_minimum_required(VERSION 3.15)
project(proj1)

set(CMAKE_CXX_STANDARD 14)

add_executable(proj1 main.cpp "ChessPieces.cpp" "ChessPieces.h" "ChessBoard.cpp" "ChessBoard.h" Setup.cpp Setup.h alphabeta.cpp alphabeta.h)