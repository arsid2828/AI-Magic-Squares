from time import perf_counter

from backtracking import solve_backtracking
from simulated_annealing import solve_simulated_annealing
from genetic_algorithm import solve_genetic_algorithm

from magic_square import print_square, is_magic_square


def read_fixed_cells(n):
    count = int(input("\nNumber of fixed cells: "))

    if count < 0 or count > n*n:
        raise ValueError("Invalid number of fixed cells")

    fixed_cells = {}
    used = set()

    for i in range(count):
        
        values = input(f"Cell {i+1} (row col value): ").split()

        if len(values) != 3:
            raise ValueError("Enter exactly 3 values: row col value")

        row, col, num = map(int, values)


        if not (1 <= row <= n and 1 <= col <= n):
            raise ValueError("Invalid cell position")

        if not 1 <= num <= n*n:
            raise ValueError("Invalid fixed value")

        position = (row-1, col-1)

        if position in fixed_cells:
            raise ValueError("Duplicate cell position")

        if num in used:
            raise ValueError("Duplicate fixed value")

        fixed_cells[position] = num
        used.add(num)

    return fixed_cells



def main():
    print("=== MAGIC SQUARE SOLVER ===")

    print("\n1. Constraint Propagation + Backtracking")
    print("2. Simulated Annealing")
    print("3. Genetic Algorithm")

    choice = input("\nChoose algorithm: ")

    if choice not in ["1", "2", "3"]:
        print("Invalid algorithm")
        return

    try:
        n = int(input("Square size N: "))
    except ValueError:
        print("N must be a positive integer")
        return

    if n < 1:
        print("N must be a positive integer")
        return
    
    if n >= 6:
        confirm = input(
            "Large squares may take a long time. Continue? (y/n): "
        ).strip().lower()

        if confirm != "y":
            print("Execution cancelled")
            return
            
    try:
        fixed_cells = read_fixed_cells(n)
    except ValueError as error:
        print("Invalid input:", error)
        return

    start = perf_counter()

    
    if choice == "1":
        square = solve_backtracking(
            n, fixed_cells=fixed_cells
        )

    elif choice == "2":
        square = solve_simulated_annealing(
            n, fixed_cells=fixed_cells
        )

    else:
        square = solve_genetic_algorithm(
            n, fixed_cells=fixed_cells
        )


    elapsed = perf_counter() - start

    print("\n=== RESULT ===")

    if square is not None:
        print_square(square)
        print("Valid:", is_magic_square(square))
        
        if fixed_cells:
            preserved = all(
                square[row][col] == num
                for (row, col), num in fixed_cells.items()
            )

            print("Fixed cells preserved:", preserved)

    
    else:
        if choice == "1":
            print("No solution exists for this configuration")
        else:
            print("No solution found within the search budget")


    print(f"Execution time: {elapsed:.5f} s")


if __name__ == "__main__":
    main()
