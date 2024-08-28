import sys

verbose = False

# Create a list to hold all possible atoms (possible values in each cell of the Sudoku grid)
ATOMS = []
for n in range(1, 10):
    for r in range(1, 10):
        for c in range(1, 10):
            # Create an atom for each possible value in each cell, formatted as 'n_r_c'
            pro_atom = 'n' + str(n) + '_r' + str(r) + '_c' + str(c)
            ATOMS.append(pro_atom)

# Initialize sets and board structure
nums_set = []
sudoku_board = []
board = []

# Initialize the Sudoku board with None values (empty cells)
for i in range(0, 9):
    b_row = []
    for j in range(0, 9):
        b_row.append(None)
    sudoku_board.append(b_row)

# Define the main DP function that solves the Sudoku puzzle based on the atoms and a set of constraints
def dp(ATOMS, S):
    V = {}
    for i in ATOMS:
        V[i] = None
    return dp1(ATOMS, S, V)

# Recursive DP function that processes the atoms and constraints
def dp1(ATOMS, S, V):
    while True:

        if not S:
            for a in ATOMS:
                if V[a] is None:
                    V[a] = False
            return V
        else:
            for clause in S:
                if not clause:
                    return None

        L = None

        # Iterate through the atoms to find an unassigned literal
        for literal in ATOMS:
            if V[literal] is None:

                found_literal, found_negation = False, False

                for clause in S:
                    if literal in clause:
                        found_literal = True
                    if "!" + literal in clause:
                        found_negation = True
                    if found_literal and found_negation:
                        break

                # After evaluating all clauses, decide on the literal
                if found_literal and (not found_negation):
                    L = literal
                    break
                elif (not found_literal) and found_negation:
                    L = "!" + literal
                    break

        # If a pure literal was found (L is assigned), process it
        if L:
            V = obviousAssign(L, V)
            S = [clause for clause in S if L not in clause]
            if verbose:
                print("easy case: pure literal " + str(atom(L)) + "=" + str(V[atom(L)]))
            continue

        # If no pure literals, look for unit clauses (clauses with only one literal)
        L = None

        for clause in S:
            if len(clause) == 1:
                L = clause[0]
                V = obviousAssign(L, V)
                S = propagate(atom(L), S, V)
                if verbose:
                    print("easy case: unit literal " + str(L))
                continue

        break

    # If no pure literals or unit clauses are found, proceed to make a guess (hard case)

    A = None
    for a in ATOMS:
        if V[a] is None:
            A = a
            orig_S = S.copy()
            orig_V = V.copy()
            S1 = S.copy()
            V[A] = True
            if verbose:
                print("Hard case: guess " + str(A) + "=true")
            # Propagate this assumption through the constraints
            S1 = propagate(A, S1, V)
            # Recursively call dp1 to continue solving with this assumption
            V_new = dp1(ATOMS, S1, V)
            if V_new is not None:
                return V_new
            S = orig_S
            V = orig_V
            if verbose:
                print("Contradiction: backtrack guess " + str(A) + "=false")
            V[A] = False
            S1 = propagate(A, orig_S, V)
            return dp1(ATOMS, S1, V)

    return None

# Helper function to assign a value to a literal in the variable assignments
def obviousAssign(L, V):
    if L[0] == '!':
        L = L[1:]
        V[L] = False
    else:
        V[L] = True

    return V

# Helper function to extract the atom from a literal (removing any negation)
def atom(L):
    if L[0] == "!":
        L = L[1:]

    return L

# Propagation function to update constraints based on the assignment of an atom
def propagate(A, S, V):
    a_neg = "!" + A
    S_new = []

    for clause in S:
        if ((A in clause) and (V[A])) or ((a_neg in clause) and (not V[A])):
            continue

        clause_to_add = clause
        if (A in clause) and (V[A] is False):
            new_clause = []
            for i in clause:
                if i != A:
                    new_clause.append(i)
            clause_to_add = new_clause
        elif (a_neg in clause) and (V[A] is True):
            new_clause = []
            for i in clause:
                if i != a_neg:
                    new_clause.append(i)
            clause_to_add = new_clause

        S_new.append(clause_to_add)

    return S_new

# Function to parse input from command-line arguments and initialize the Sudoku board
def parseInput(inp):
    for item in sys.argv:
        if "=" in item:
            if len(item) != 4:
                raise Exception(
                    'Format of input should be two digits an equals sign followed by a single digit e.g. (11=4)')
            num_and_position = "n" + item[3] + "_r" + item[0] + "_c" + item[1]
            nums_set.append(num_and_position)
            if (int(item[3]) not in range(1, 10)) or (int(item[0]) not in range(1, 10)) or (
                    int(item[1]) not in range(1, 10)):
                raise Exception("numbers and coordinates must be in the range 1-9")

        if "-v" == item:
            global verbose
            verbose = True

    # Put initial values into board rest are None
    for num in nums_set:
        value = int(num[1])
        row = int(num[4]) - 1
        column = int(num[7]) - 1
        sudoku_board[row][column] = value

    return sudoku_board

# Function to generate the constraints for the Sudoku puzzle
def sudokuContraints(board):
    # clauses will be a list of list every sentence will be a list
    clauses = []

    # Loop through initial board and add clause as a single list to clauses
    for r in range(0, 9):
        for c in range(0, 9):
            if board[r][c]:
                v = board[r][c]
                clause = []
                c_to_add = 'n' + str(v) + '_r' + str(r + 1) + '_c' + str(c + 1)
                clause.append(c_to_add)
                clauses.append(clause)

    # At least one digit in a box
    for r in range(1, 10):
        for c in range(1, 10):
            clause = []
            for v in range(1, 10):
                sentence = 'n' + str(v) + '_r' + str(r) + '_c' + str(c)
                clause.append(sentence)
            clauses.append(clause)

    # Unique row
    for r in range(1, 10):
        for v in range(1, 10):
            for c in range(1, 10):
                for not_c in range(1, 10):
                    clause = []
                    if c != not_c:
                        clause_1 = '!n' + str(v) + '_r' + str(r) + '_c' + str(c)
                        clause_2 = '!n' + str(v) + '_r' + str(r) + '_c' + str(not_c)
                        clause.append(clause_1)
                        clause.append(clause_2)
                        clauses.append(clause)

    # Unique column
    for c in range(1, 10):
        for v in range(1, 10):
            for r in range(1, 10):
                for not_r in range(1, 10):
                    clause = []
                    if r != not_r:
                        clause_1 = '!n' + str(v) + '_r' + str(r) + '_c' + str(c)
                        clause_2 = '!n' + str(v) + '_r' + str(not_r) + '_c' + str(c)
                        clause.append(clause_1)
                        clause.append(clause_2)
                        clauses.append(clause)

    # Unique 3x3
    for v in range(1, 10):
        for block_r in range(3):
            for block_c in range(3):
                for r in range(1, 4):
                    for not_r in range(1, 4):
                        for c in range(1, 4):
                            for not_c in range(1, 4):
                                clause = []
                                if (r != not_r) and (c != not_c):
                                    real_r = 3 * block_r + r
                                    real_c = 3 * block_c + c
                                    real_not_r = 3 * block_r + not_r
                                    real_not_c = 3 * block_c + not_c

                                    clause_1 = '!n' + str(v) + '_r' + str(real_r) + '_c' + str(real_c)
                                    clause_2 = '!n' + str(v) + '_r' + str(real_not_r) + '_c' + str(real_not_c)
                                    clause.append(clause_1)
                                    clause.append(clause_2)
                                    clauses.append(clause)

    return clauses


def convertBack(assignments):
    global board
    if assignments:
        for i in assignments:
            if assignments[i]:
                v = i[1]
                r = int(i[4]) - 1
                c = int(i[7]) - 1
                board[r][c] = int(v)
    else:
        board = "NO VALID ASSIGNMENT"

    return board


board = parseInput(sys.argv)

clauses = sudokuContraints(board)

assignments = dp(ATOMS, clauses)

solution = convertBack(assignments)

if solution != "NO VALID ASSIGNMENT":
    for board_row in solution:
        for i in board_row:
            print(' ' + str(i) + ' ', end="")
        print()
else:
    print(solution)
