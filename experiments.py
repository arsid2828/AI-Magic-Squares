
from time import perf_counter
from statistics import median

from backtracking import solve_backtracking
from simulated_annealing import solve_simulated_annealing
from genetic_algorithm import solve_genetic_algorithm
from magic_square import is_magic_square


cases = [
    ("3x3", 3, {}),
    ("3x3 fixed", 3, {(0, 0): 8, (1, 1): 5, (2, 2): 2}),
    ("4x4", 4, {}),
    ("4x4 fixed", 4, {(0, 0): 16, (1, 1): 11, (2, 2): 6}),
    ("5x5", 5, {}),
    ("5x5 fixed", 5, {(0, 0): 17, (2, 2): 13, (4, 4): 9})
]


algorithms = [
    "CP + Backtracking + MRV",
    "Simulated Annealing",
    "Genetic Algorithm"
]

runs=20

for case_name, n, fixed_cells in cases:
    print(f"\n=== {case_name.upper()} ===")

    for algorithm in algorithms:
        times = []
        successful_times = []

        for seed in range(runs):
            start = perf_counter()

            if algorithm == "CP + Backtracking + MRV":
                square = solve_backtracking(
                    n, use_mrv=True, use_lcv=False,
                    fixed_cells=fixed_cells
                )

            elif algorithm == "Simulated Annealing":
                square = solve_simulated_annealing(
                    n, fixed_cells=fixed_cells, seed=seed
                )

            else:
                square = solve_genetic_algorithm(
                    n, fixed_cells=fixed_cells, seed=seed
                )

            elapsed = perf_counter() - start
            times.append(elapsed)

            if square is not None:
                valid = is_magic_square(square) and all(
                    square[row][col] == num
                    for (row, col), num in fixed_cells.items()
                )

                if not valid:
                    raise RuntimeError(f"{algorithm}: invalid solution")

                successful_times.append(elapsed)

        success_rate = len(successful_times) / runs * 100

        print(f"\n{algorithm}")
        print(f"Success rate: {success_rate:.1f}% ({len(successful_times)}/{runs})")
        print(f"Median time (all runs): {median(times):.5f} s")

        if successful_times:
            print(f"Median time (successful runs): {median(successful_times):.5f} s")
        else:
            print("Median time (successful runs): N/A")
