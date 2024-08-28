# Sudoku-Solver-Using-Predicate-Logic
This python project implements a Sudoku solver leveraging predicate logic to represent and solve the puzzle 


To run use the following command:

python3 sudoku_solver.py [-v] 12=5 14=3 ..

Where -v is optional for verbose 

The code may run slowly for some of the case scenarios especially with verbose 

Medium input too 10-20 minutes, Easy, hw1 and evil were shorter.

Expert and hard inputs too very long around an hour each


A sample run will look like:

Input:

python3 sudoku.py 11=4 12=5 23=2 25=7 27=6 28=3 38=2 39=8 44=9 45=5 52=8 53=6 57=2 62=2 64=6 67=7 68=5 77=4 78=7 79=6 82=7 85=4 86=5 93=8 96=9

Output:

 4  5  3  8  2  6  1  9  7
 
 8  9  2  5  7  1  6  3  4 
 
 1  6  7  4  9  3  5  2  8 
 
 7  1  4  9  5  2  8  6  3 
 
 5  8  6  1  3  7  2  4  9 
 
 3  2  9  6  8  4  7  5  1 
 
 9  3  5  2  1  8  4  7  6 
 
 6  7  1  3  4  5  9  8  2 
 
 2  4  8  7  6  9  3  1  5 
