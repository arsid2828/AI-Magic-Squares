
from multiprocessing import get_context
from statistics import median
from time import perf_counter

from backtracking import solve_backtracking
from magic_square import is_magic_square


# Keep these identical to experiments.py; importing it would run its benchmarks.
cases = [
    ("3x3", 3, {}),
    ("3x3 fixed", 3, {(0, 0): 8, (0, 1): 1}),
    ("4x4", 4, {}),
    ("4x4 fixed", 4, {(0, 0): 16, (0, 3): 13, (1, 0): 5, (2, 3): 12}),
    ("5x5", 5, {}),
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

methods = [
    ("CP + Backtracking + MRV", False),
    ("CP + Backtracking + MRV + LCV", True),
]
runs = 3
time_limit = 30.0


def _solve_worker(connection, n, fixed_cells, use_lcv, deadline):
    try:
        start = perf_counter()
        remaining = deadline - start
        if remaining <= 0:
            raise TimeoutError("Execution deadline exceeded")
        square = solve_backtracking(
            n, use_mrv=True, use_lcv=use_lcv,
            fixed_cells=fixed_cells, time_limit=remaining,
        )
        connection.send(("result", perf_counter() - start, square))
    except TimeoutError:
        connection.send(("timeout", None, None))
    except Exception as error:
        connection.send(("error", None, repr(error)))
    finally:
        connection.close()


def run_execution(n, fixed_cells, use_lcv, limit=time_limit):
    context = get_context("spawn")
    receiver, sender = context.Pipe(duplex=False)
    deadline = perf_counter() + limit
    process = context.Process(
        target=_solve_worker,
        args=(sender, n, fixed_cells, use_lcv, deadline),
    )
    try:
        process.start()
        sender.close()
        remaining = max(0.0, deadline - perf_counter())
        if not receiver.poll(remaining):
            return "timeout", limit, None
        try:
            status, elapsed, square = receiver.recv()
        except EOFError as error:
            raise RuntimeError("Solver worker exited without a result") from error
        if status == "error":
            raise RuntimeError(f"Solver worker failed: {square}")
        if status == "timeout" or perf_counter() >= deadline:
            return "timeout", limit, None
        return status, elapsed, square
    finally:
        # Never leave a timed-out (or interrupted) solver running in the background.
        if process.pid is not None:
            try:
                if process.is_alive():
                    process.terminate()
                process.join(timeout=1.0)
                if process.is_alive():
                    process.kill()
                    process.join()
            finally:
                process.close()
        receiver.close()
        sender.close()


def main():
    header = (f"{'Case':<10} {'Method':<32} {'Median (all)':>13} "
              f"{'Median (success)':>17} {'Successes':>10} {'Timeouts':>10}")

    for n in range(3, 9):
        print(f"\n=== MAGIC SQUARE {n}x{n} ===")
        print(header)
        print("-" * len(header))
        for _, size, fixed_cells in cases:
            if size != n:
                continue
            case_label = "Fixed" if fixed_cells else "Non-Fixed"
            for name, use_lcv in methods:
                times = []
                successful_times = []
                timeouts = 0
                for _ in range(runs):
                    status, elapsed, square = run_execution(n, fixed_cells, use_lcv)
                    times.append(elapsed)
                    if status == "timeout":
                        timeouts += 1
                    elif square is not None:
                        valid = (
                            len(square) == n and is_magic_square(square)
                            and all(square[row][col] == value
                                    for (row, col), value in fixed_cells.items())
                        )
                        if not valid:
                            raise RuntimeError(f"{n}x{n} {case_label}, {name}: invalid solution")
                        successful_times.append(elapsed)

                success_median = (f"{median(successful_times):.5f}"
                                  if successful_times else "N/A")
                print(f"{case_label:<10} {name:<32} {median(times):>13.5f} "
                      f"{success_median:>17} "
                      f"{len(successful_times):>8}/{runs} {timeouts:>8}/{runs}",
                      flush=True)


if __name__ == "__main__":
    main()
