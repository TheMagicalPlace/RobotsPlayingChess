cmake_minimum_required(VERSION 3.15)
project(RobotsPlayingChess)

set(CMAKE_CXX_STANDARD 14)




add_executable(RobotsPlayingChess ${PROJECT_SOURCE_DIR}/main.cpp
        ${PROJECT_SOURCE_DIR}/src/ChessPieces.cpp
        ${PROJECT_SOURCE_DIR}/src/Setup.cpp
        ${PROJECT_SOURCE_DIR}/src/alphabeta.cpp src/CppPythonCrossModule.cpp headers/CppPythonCrossModule.h)



include_directories(
        "${PROJECT_SOURCE_DIR}/headers"
)