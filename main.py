
from backtracking import solve_backtracking
from magic_square import print_square, is_magic_square

def main():
    n = 3

    fixed_cells = {
        (0, 0): 8,
        (1, 1): 5,
        (2, 2): 2
    }

    square = solve_backtracking(
        n,
        use_mrv=True,
        use_lcv=True,
        fixed_cells=fixed_cells
    )

    if square is not None:
        print_square(square)
        print("Valid:", is_magic_square(square))

        preserved = all(
            square[row][col] == num
            for (row, col), num in fixed_cells.items()
        )
        print("Fixed cells preserved:", preserved)
    else:
        print("No solution found")

if __name__ == "__main__":
    main()

