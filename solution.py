rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]

def diag_cross(a, b):
    return [a[i] + b[i] for i in range(0,9,1)]

boxes = cross(rows, cols)

diag_cross_vals = diag_cross(rows,cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [diag_cross_vals]
unitlist = row_units + column_units + square_units + diag_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)

square_units = dict((s, [u for u in square_units if s in u]) for s in boxes)
row_units = dict((s, [u for u in row_units if s in u]) for s in boxes)
column_units = dict((s, [u for u in column_units if s in u]) for s in boxes)

diag_peers = dict()

diag_peers['A1'] = ['B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']
diag_peers['B2'] = ['A1', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']
diag_peers['C3'] = ['A1', 'B2', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']
diag_peers['D4'] = ['A1', 'B2', 'C3', 'E5', 'F6', 'G7', 'H8', 'I9']
diag_peers['E5'] = ['A1', 'B2', 'C3', 'D4', 'F6', 'G7', 'H8', 'I9']
diag_peers['F6'] = ['A1', 'B2', 'C3', 'D4', 'E5', 'G7', 'H8', 'I9']
diag_peers['G7'] = ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'H8', 'I9']
diag_peers['H8'] = ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'I9']
diag_peers['I9'] = ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8']


square_peers = dict((s, set(sum(square_units[s],[]))-set([s])) for s in boxes)
row_peers = dict((s, set(sum(row_units[s],[]))-set([s])) for s in boxes)
column_peers = dict((s, set(sum(column_units[s],[]))-set([s])) for s in boxes)

peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)





def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]

def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

        Args:
            grid: Sudoku grid in string form, 81 characters long
        Returns:
            Sudoku grid in dictionary form:
            - keys: Box labels, e.g. 'A1'
            - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
        """
    values = []
    all_digits = '123456789'
    valIdx = 0
    for c in grid:
        valIdx = valIdx + 1
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)


    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    #First, find all twins

    stalled = False
    while not stalled:

        initial_values = values
        for box in values:



            digit = values[box]
            if(len(digit) != 2) :
                continue


            for row_peer in row_peers[box]:
                peer_value = values[row_peer]
                if(len(peer_value) != 2) :
                    continue
                if digit == peer_value :
                    #print("Match")
                    #print("Digit is: "+digit)
                    #print("peer_value: "+peer_value)
                    #print("peer is: "+peer)
                    #print("box is: "+box)
                    # Go thru peers again, removing unneeded values
                    for inner_peer in row_peers[box] :
                        if inner_peer == box or inner_peer == row_peer :
                            continue
                        for chr in digit :
                            if len(values[inner_peer]) > 1:
                                values[inner_peer] = values[inner_peer].replace(chr, '')

            for column_peer in column_peers[box]:
                #print(column_peer)
                peer_value = values[column_peer]
                if(len(peer_value) != 2) :
                    continue
                if digit == peer_value :
                    #print("Match")
                    #print("Digit is: "+digit)
                    #print("peer_value: "+peer_value)
                    #print("peer is: "+peer)
                    #print("box is: "+box)
                    # Go thru peers again, removing unneeded values
                    for inner_peer in column_peers[box] :
                        if inner_peer == box or inner_peer == column_peer :
                            continue
                        for chr in digit :
                            if len(values[inner_peer]) > 1:
                                values[inner_peer] = values[inner_peer].replace(chr, '')

            if box in diag_cross_vals :
                for diag_peer in diag_peers[box]:
                    #print(column_peer)
                    peer_value = values[diag_peer]
                    if(len(peer_value) != 2) :
                        continue
                    if digit == peer_value :
                        #print("Match")
                        #print("Digit is: "+digit)
                        #print("peer_value: "+peer_value)
                        #print("peer is: "+peer)
                        #print("box is: "+box)
                        # Go thru peers again, removing unneeded values
                        for inner_peer in diag_peers[box] :
                            if inner_peer == box or inner_peer == diag_peer :
                                continue
                            for chr in digit :
                                if len(values[inner_peer]) > 1:
                                    values[inner_peer] = values[inner_peer].replace(chr, '')


            for square_peer in square_peers[box]:
                #print(column_peer)
                peer_value = values[square_peer]
                if(len(peer_value) != 2) :
                    continue
                if digit == peer_value :
                    #print("Match")
                    #print("Digit is: "+digit)
                    #print("peer_value: "+peer_value)
                    #print("peer is: "+peer)
                    #print("box is: "+box)
                    # Go thru peers again, removing unneeded values
                    for inner_peer in square_peers[box] :
                        if inner_peer == box or inner_peer == square_peer :
                            continue
                        for chr in digit :
                            if len(values[inner_peer]) > 1:
                                values[inner_peer] = values[inner_peer].replace(chr, '')

        final_values = values
        if initial_values == final_values :
            stalled = True


    return values



def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]

        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """
        Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
        If the sudoku is solved, return the sudoku.
        If after an iteration of both functions, the sudoku remains the same, return the sudoku.
        Input: A sudoku in dictionary form.
        Output: The resulting sudoku in dictionary form.
        """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])



        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)

        # Use the naked twins strategy
        values = naked_twins(values)


        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    grid_dict = grid_values(grid)
    # print(grid_dict)
    return_val = search(grid_dict)
    # print(return_val)
    return return_val

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    normal_sudoku_grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'


    #solved_puzzle = solve(diag_sudoku_grid)
    #print(solved_puzzle)
    #if(solved_puzzle is not None) :
    #    display(solved_puzzle)
    #else :
    #    print("Could not solve puzzle")
    #    exit(0)

