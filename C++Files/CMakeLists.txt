cmake_minimum_required(VERSION 3.15)
project(RobotsPlayingChess)

set(CMAKE_CXX_STANDARD 14)




add_executable(RobotsPlayingChess ${PROJECT_SOURCE_DIR}/main.cpp
        ${PROJECT_SOURCE_DIR}/src/ChessPieces.cpp
        ${PROJECT_SOURCE_DIR}/src/Setup.cpp
        ${PROJECT_SOURCE_DIR}/src/alphabeta.cpp
        ${PROJECT_SOURCE_DIR}/src/CppPythonCrossModule.cpp)



include_directories(
        "${PROJECT_SOURCE_DIR}/headers"
        "C:\\Users\\themagicalplace\\AppData\\Local\\Programs\\Python\\Python38\\include\\"
        "C:\\Users\\themagicalplace\\AppData\\Local\\Programs\\Python\\Python38\\"
)