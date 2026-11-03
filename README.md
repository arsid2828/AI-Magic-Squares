# **AI MAGIC SQUARES**

This project solves N×N Magic Squares using Constraint Propagation with Backtracking, Simulated Annealing, and Genetic Algorithm. It also supports partially filled squares with fixed cells.

## Requirements:

Python 3. No external libraries required.

## Run the solver:

python main.py

Choose an algorithm, enter the square size, and specify the number of fixed cells (0 for none). Each cell is entered as row col value, using 1-based row and column positions.

The interactive solver has no wall-clock time limit. Simulated Annealing and Genetic Algorithm still have their temperature, iteration, and generation stopping criteria. Backtracking uses MRV, with LCV disabled.

## Run the experiments:

python experiments.py

This compares the three algorithms on 3x3 through 8x8 squares, with and without fixed cells. 

For the fixed-cell configurations, approximately 25% of the cells are preassigned. Each algorithm is executed 20 times for each of the 12 test cases, resulting in 720 executions.

Simulated Annealing and Genetic Algorithm use seeds 0 through 19. Backtracking is deterministic; its repeated runs measure execution time.

All three algorithms have the same 30-second limit per run, checked periodically during the search. A run may slightly exceed this limit. Simulated Annealing and Genetic Algorithm can stop earlier at their existing search limits.

The output reports success counts, timeout counts, the median time over all runs (including timeouts and other unsuccessful runs), and the median time over successful runs. A timeout does not establish that the problem has no solution. Twenty timeouts can take about ten minutes for one algorithm on one case.

Results are printed to the terminal. To save them in results.txt, run:

python -u experiments.py > results.txt

Run the final experiment set sequentially on the same computer, and record the Python version and computer specifications for the report.

### For a separate comparison of backtracking heuristics:

python compare_backtracking.py

Both configurations are tested on Magic Squares from 3×3 to 8×8, with and without fixed cells, using the same test cases as the main experiments.
