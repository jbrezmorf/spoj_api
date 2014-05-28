#!/bin/bash

# bash 28
echo "====================== TEST Bash"
#python spoj_run.py TEST 28 test.bash.src

# python 4
echo "====================== TEST Python"
#python spoj_run.py TEST 4 test.python.src

# C++ 41
echo "====================== TEST C++ Accepted"
#python spoj_run.py TEST 41 test_accepted.cpp

echo "====================== TEST C++ Wrong answer"
#python spoj_run.py TEST 41 test_wrong.cpp

echo "====================== TEST C++ Run error"
python spoj_run.py SEGMENT 41 test_run_err_SEGV.cpp

#python spoj_run.py SEGMENT 41 test_run_err.cpp

echo "====================== TEST C++ Compile error"
#python spoj_run.py SEGMENT 41 test_compile_err.cpp
