
from time import perf_counter
from statistics import median

from backtracking import solve_backtracking
from simulated_annealing import solve_simulated_annealing
from genetic_algorithm import solve_genetic_algorithm
from magic_square import is_magic_square


cases=[
    ("3x3",3,{}),
    ("3x3 fixed", 3, {(0, 0): 8, (0, 1): 1}),
    ("4x4",4,{}),
    ("4x4 fixed", 4, {(0, 0): 16, (0, 3): 13, (1, 0): 5, (2, 3): 12}),
    ("5x5",5,{}),
    ("5x5 fixed", 5, {(0, 0): 17, (0, 3): 8, (1, 2): 7,
                       (1, 3): 14, (4, 0): 11, (4, 4): 9}),
    ("6x6", 6, {}),
    ("6x6 fixed", 6, {(0, 1): 1, (0, 3): 26, (0, 4): 19,
                       (1, 1): 32, (2, 2): 2, (2, 3): 22,
                       (2, 5): 20, (3, 3): 17, (3, 5): 15}),
    ("7x7", 7, {}),
    ("7x7 fixed", 7, {(0, 1): 39, (0, 5): 19, (0, 6): 28,
                       (1, 0): 38, (1, 1): 47, (2, 0): 46,
                       (2, 1): 6, (2, 3): 17, (3, 6): 45,
                       (4, 6): 4, (5, 2): 32, (5, 5): 3}),
    ("8x8", 8, {}),
    ("8x8 fixed", 8, {(0, 1): 2, (0, 2): 3, (0, 5): 6, (0, 6): 7,
                       (1, 0): 9, (1, 6): 50, (1, 7): 16, (2, 1): 47,
                       (3, 3): 37, (4, 2): 35, (4, 5): 38, (5, 3): 44,
                       (5, 7): 48, (7, 0): 8, (7, 5): 62, (7, 7): 1}),
]


algorithms=[
    "CP + Backtracking + MRV",
    "Simulated Annealing",
    "Genetic Algorithm"
]

runs=20
time_limit=30.0

for case_name,n,fixed_cells in cases:
    print(f"\n=== {case_name.upper()} ===")

    for algorithm in algorithms:
        times=[]
        successful_times=[]
        timeouts = 0
        for seed in range(runs):
            start = perf_counter()

            try:
                if algorithm == "CP + Backtracking + MRV":
                    square = solve_backtracking(
                        n,
                        use_mrv=True,
                        use_lcv=False,
                        fixed_cells=fixed_cells,
                        time_limit=time_limit
                    )

                elif algorithm== "Simulated Annealing":
                    square=solve_simulated_annealing(
                        n,fixed_cells=fixed_cells, seed=seed,
                        time_limit=time_limit
                    )

                else:
                    square=solve_genetic_algorithm(
                        n,fixed_cells=fixed_cells, seed=seed,
                        time_limit=time_limit
                    )
            except TimeoutError:
                square = None
                timeouts += 1

            elapsed=perf_counter()-start
            times.append(elapsed)

            if square is not None:
                valid=is_magic_square(square) and all(
                    square[row][col]==num
                    for (row, col),num in fixed_cells.items()
                )

                if not valid:
                    raise RuntimeError(f"{algorithm}: invalid solution")

                successful_times.append(elapsed)

        success_rate=len(successful_times)/runs*100

        print(f"\n{algorithm}")
        print(f"Success rate: {success_rate:.1f}% ({len(successful_times)}/{runs})")
        print(f"Timeouts: {timeouts}/{runs}")
        print(f"Time limit: {time_limit:g} s")
        if algorithm == "CP + Backtracking + MRV":
            print("MRV: True, LCV: False")
        print(f"Median time (all runs): {median(times):.5f} s")

        if successful_times:
            print(f"Median time (successful runs): {median(successful_times):.5f} s")
        else:
            print("Median time (successful runs): N/A")
