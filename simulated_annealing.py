
import random
from math import exp
from magic_square import magic_constant


#Calculate the total error of all rows, columns and diagonals
def magic_cost(square):
    n = len(square)
    target = magic_constant(n)

    cost = 0

    #Row errors
    for row in square:
        cost += abs(sum(row) - target)

    #Column errors
    for col in range(n):
        column_sum = sum(square[row][col] for row in range(n))
        cost += abs(column_sum - target)

    #Diagonal errors
    main_diagonal = sum(square[i][i] for i in range(n))
    secondary_diagonal = sum(square[i][n-1-i] for i in range(n))

    cost += abs(main_diagonal - target)
    cost += abs(secondary_diagonal - target)

    return cost


#Generate a random complete square while preserving fixed cells
def random_square(n, fixed_cells=None, rng=None):
    if type(n) is not int or n < 1:
        raise ValueError("n must be a positive integer")

    if fixed_cells is None:
        fixed_cells = {}

    if rng is None:
        rng = random.Random()

    square = [[0]*n for _ in range(n)]
    used = set()

    #Place and validate fixed values
    for position, num in fixed_cells.items():
        if (not isinstance(position, tuple) or len(position) != 2
            or any(type(x) is not int for x in position)):
            raise ValueError("Invalid cell position")

        row, col = position

        if not (0 <= row < n and 0 <= col < n):
            raise ValueError("Cell position outside the square")

        if type(num) is not int or not (1 <= num <= n*n):
            raise ValueError("Invalid fixed value")

        if num in used:
            raise ValueError("Duplicate fixed value")

        square[row][col] = num
        used.add(num)

    #Shuffle the remaining numbers
    remaining = [
        num for num in range(1, n*n+1)
        if num not in used
    ]
    rng.shuffle(remaining)

    #Fill the empty cells with the shuffled numbers
    values = iter(remaining)

    for row in range(n):
        for col in range(n):
            if square[row][col] == 0:
                square[row][col] = next(values)

    return square


#Generate a neighboring state by swapping two non-fixed cells
def random_neighbor(square, fixed_cells=None, rng=None):
    if fixed_cells is None:
        fixed_cells = {}

    if rng is None:
        rng = random.Random()

    n = len(square)

    #Create an independent copy to preserve the original state
    neighbor = [row[:] for row in square]

    #Find all positions that can be modified
    movable = [
        (row, col)
        for row in range(n)
        for col in range(n)
        if (row, col) not in fixed_cells
    ]

    #A swap requires at least two movable cells
    if len(movable) < 2:
        return neighbor

    #Select two different positions randomly
    (r1, c1), (r2, c2) = rng.sample(movable, 2)

    #Swap their values
    neighbor[r1][c1], neighbor[r2][c2] = (
        neighbor[r2][c2], neighbor[r1][c1]
    )

    return neighbor


#Decide whether to accept a neighboring state
def accept_neighbor(delta, temperature, rng):

    #Always accept improvements or equal-cost moves
    if delta <= 0:
        return True

    if temperature <= 0:
        raise ValueError("Temperature must be positive")

    #Accept worse moves with a temperature-dependent probability
    probability = exp(-delta / temperature)

    return rng.random() < probability


#Solve a magic square using Simulated Annealing
def solve_simulated_annealing(n, fixed_cells=None,
                             initial_temperature=10.0,
                             cooling_rate=0.9995,
                             min_temperature=0.01,
                             max_iterations=50000,
                             seed=None):

    if initial_temperature <= 0 or min_temperature <= 0:
        raise ValueError("Temperatures must be positive")

    if not 0 < cooling_rate < 1:
        raise ValueError("Cooling rate must be between 0 and 1")

    if type(max_iterations) is not int or max_iterations < 0:
        raise ValueError("Invalid maximum iterations")

    if fixed_cells is None:
        fixed_cells = {}

    #Use a dedicated random generator for reproducible experiments
    rng = random.Random(seed)

    #Generate the initial state
    current = random_square(n, fixed_cells, rng)
    current_cost = magic_cost(current)

    #Remember the best state found during the search
    best = [row[:] for row in current]
    best_cost = current_cost

    temperature = initial_temperature

    #Main Simulated Annealing loop
    for _ in range(max_iterations):

        #Stop immediately when a magic square is found
        if best_cost == 0:
            return best

        #Stop when the temperature becomes too low
        if temperature < min_temperature:
            break

        #Generate and evaluate a neighboring state
        neighbor = random_neighbor(current, fixed_cells, rng)
        neighbor_cost = magic_cost(neighbor)

        delta = neighbor_cost - current_cost

        #Accept improvements and some worse moves
        if accept_neighbor(delta, temperature, rng):
            current = neighbor
            current_cost = neighbor_cost

            #Store the best solution independently
            if current_cost < best_cost:
                best = [row[:] for row in current]
                best_cost = current_cost

        #Geometric cooling schedule
        temperature *= cooling_rate

    #Return None if no valid magic square was found
    return best if best_cost == 0 else None



if __name__ == "__main__":
    from magic_square import print_square, is_magic_square

    fixed_cells = {
        (0, 0): 8,
        (1, 1): 5,
        (2, 2): 2
    }

    square = solve_simulated_annealing(
        n=3,
        fixed_cells=fixed_cells,
        seed=42
    )

    if square is not None:
        print("=== SIMULATED ANNEALING ===")
        print_square(square)
        print("Cost:", magic_cost(square))
        print("Valid:", is_magic_square(square))

        preserved = all(
            square[row][col] == num
            for (row, col), num in fixed_cells.items()
        )
        print("Fixed cells preserved:", preserved)
    else:
        print("No valid solution found")
