
from time import perf_counter
from statistics import median

from simulated_annealing import solve_simulated_annealing
from magic_square import is_magic_square


#Test different square sizes and initial configurations
cases = [
    (3, None),
    (3, {(0, 0): 8, (1, 1): 5, (2, 2): 2}),
    (4, None)
]

for n, fixed_cells in cases:
    print(f"\n=== SIMULATED ANNEALING {n}x{n} ===")
    print("Fixed cells:", fixed_cells)

    times = []
    successes = 0
    runs = 10

    #Repeat the experiment with different random seeds
    for seed in range(runs):
        start = perf_counter()

        square = solve_simulated_annealing(
            n=n,
            fixed_cells=fixed_cells,
            seed=seed
        )

        elapsed = perf_counter() - start
        times.append(elapsed)

        if square is not None:
            #Check solution validity and fixed cell preservation
            valid = is_magic_square(square)

            if fixed_cells is not None:
                valid = valid and all(
                    square[row][col] == num
                    for (row, col), num in fixed_cells.items()
                )

            if not valid:
                raise RuntimeError("Invalid solution returned")

            successes += 1

    #Calculate success rate and median execution time
    success_rate = successes / runs * 100

    print(f"Success rate: {success_rate:.1f}%")
    print(f"Median time: {median(times):.5f} s")
