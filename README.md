# **AI MAGIC SQUARES**

This project solves N×N Magic Squares using Constraint Propagation with Backtracking, Simulated Annealing, and Genetic Algorithm. It also supports partially filled squares with fixed cells.

## Requirements:

Python 3. No external libraries required.

## Run the solver:

python main.py

Choose an algorithm, enter the square size, and specify the number of fixed cells (0 for none). Each cell is entered as row col value, using 1-based row and column positions.

## Run the experiments:

python experiments.py

This compares the three algorithm on 3x3, 4x4, 5x5 squares with and without fixed cells, using 20 runs per case. The recorded results are in results.txt.

### For a separate comparison of backtracking heuristics:

python compare_backtracking.py
