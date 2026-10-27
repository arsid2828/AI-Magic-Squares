
from time import perf_counter
from statistics import median

from genetic_algorithm import solve_genetic_algorithm
from magic_square import is_magic_square

cases = [
    (3, None),
    (3, {(0, 0): 8, (1, 1): 5, (2, 2): 2}),
    (4, None)
]

for n, fixed_cells in cases:
    print(f"\n=== GENETIC ALGORITHM {n}x{n} ===")
    print("Fixed cells:", fixed_cells)

    times = []
    successes = 0
    runs = 5

    for seed in range(runs):
        start = perf_counter()

        square = solve_genetic_algorithm(
            n=n,
            fixed_cells=fixed_cells,
            population_size=40,
            max_generations=1000,
            mutation_rate=0.2,
            seed=seed
        )

        elapsed = perf_counter() - start
        times.append(elapsed)

        if square is not None:
            valid = is_magic_square(square)

            if fixed_cells is not None:
                valid = valid and all(
                    square[row][col] == num
                    for (row, col), num in fixed_cells.items()
                )

            if not valid:
                raise RuntimeError("Invalid solution returned")

            successes += 1

        print(f"Seed {seed}: {'Success' if square is not None else 'Failed'}")

    success_rate = successes / runs * 100

    print(f"Success rate: {success_rate:.1f}%")
    print(f"Median time: {median(times):.5f} s")
