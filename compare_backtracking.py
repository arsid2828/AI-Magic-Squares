
from time import perf_counter
from statistics import median

from backtracking import solve_backtracking
from magic_square import is_magic_square

methods = [
    ("CP + Backtracking", False, False),
    ("CP + Backtracking + MRV", True, False),
    ("CP + Backtracking + MRV + LCV", True, True)
]
#compare the algorithms on different square sizes
for n in [3, 4]:
    print(f"\n=== MAGIC SQUARE {n}x{n} ===")

    for name, mrv, lcv in methods:
        times = []

        for _ in range(5):
            start = perf_counter()

            square = solve_backtracking(
                n, use_mrv=mrv, use_lcv=lcv
            )

            elapsed = perf_counter() - start
            times.append(elapsed)

            if square is None or not is_magic_square(square):
                raise RuntimeError(f"{name}: invalid result")

        print(f"{name}: {median(times):.5f} s")
