
from magic_square import magic_constant, is_magic_square
#solve a NxN magic square using Constraint propagation and backtracking
#MRV and LCV can be enabled independently
#fixed cells are optional and cannot be modified by the solver
def solve_backtracking(n, use_mrv=True, use_lcv=False, fixed_cells=None):
    if type(n) is not int or n < 1:
        raise ValueError("n must be a positive integer")
    
    square = [[0]*n for _ in range(n)]
    used = set()
    target = magic_constant(n)
    
    
    #initialize fixed cells
    if fixed_cells is None:
        fixed_cells = {}

    for position, num in fixed_cells.items():
        #validate coordinates and their values
        if (not isinstance(position, tuple) or len(position) != 2
            or any(type(x) is not int for x in position)):
            raise ValueError("Invalid cell position")

        row, col = position

        if not (0 <= row < n and 0 <= col < n):
            raise ValueError("Cell position outside the square")

        if type(num) is not int or not (1 <= num <= n*n):
            raise ValueError("Invalid fixed value")

        
        if num in used:
            raise ValueError("Duplicate fixed value")


        square[row][col] = num
        used.add(num)
#check whether the assignment at row,col is compatible with row, column and diagonal sum constraints
    def valid_partial(row, col):
        lines = [
            square[row],
            [square[i][col] for i in range(n)]
        ]

        if row == col:
            lines.append([square[i][i] for i in range(n)])

        if row + col == n-1:
            lines.append([square[i][n-1-i] for i in range(n)])

        
        current_num = square[row][col]

        available = [
            num for num in range(1, n*n+1)
            if num not in used and num != current_num
        ]

        for line in lines:
            total = sum(line)
            missing = line.count(0)

            if missing == 0:
                if total != target:
                    return False
                continue
            #bound the possible final sum using smallest and largest available numbers
            minimum = total + sum(available[:missing])
            maximum = total + sum(available[-missing:])

            if minimum > target or maximum < target:
                return False

        return True


    #compute the domain of every unassigned variable
    #return none if at least one cell has no legal candidates
    def calculate_domains():
        available = [
            num for num in range(1, n*n+1)
            if num not in used
        ]

        domains = {}

        for row in range(n):
            for col in range(n):
                if square[row][col] != 0:
                    continue

                candidates = []

                for num in available:
                    square[row][col] = num

                    if valid_partial(row, col):
                        candidates.append(num)

                    square[row][col] = 0

                if not candidates:
                    return None

                domains[(row, col)] = candidates

        return domains

    #repeatedly reduce variable domains using the constraints
    #stop when no domain changes or a contradiction is detected
    def propagate_domains():
        domains = calculate_domains()

        if domains is None:
            return None

        #build all rows, columns and diagonals
        lines = []

        for i in range(n):
            lines.append([(i, j) for j in range(n)])
            lines.append([(j, i) for j in range(n)])

        lines.append([(i, i) for i in range(n)])
        lines.append([(i, n-1-i) for i in range(n)])

        changed = True

        while changed:
            changed = False

            #propagate singleton domains
            singles = [
                values[0]
                for values in domains.values()
                if len(values) == 1
            ]

            if len(singles) != len(set(singles)):
                return None

            for cell, values in domains.items():
                if len(values) > 1:
                    new_values = [
                        v for v in values if v not in singles
                    ]

                    if not new_values:
                        return None

                    if len(new_values) < len(values):
                        domains[cell] = new_values
                        changed = True

            #propagate sum constraints
            for line in lines:
                empty = [
                    cell for cell in line
                    if cell in domains
                ]

                total = sum(square[r][c] for r, c in line)

                if not empty:
                    if total != target:
                        return None
                    continue

                for cell in empty:
                    others = [c for c in empty if c != cell]

                    min_other = sum(
                        min(domains[c]) for c in others
                    )
                    max_other = sum(
                        max(domains[c]) for c in others
                    )

                    values = domains[cell]

                    new_values = [
                        v for v in values
                        if total + v + min_other <= target
                        <= total + v + max_other
                    ]

                    if not new_values:
                        return None

                    if len(new_values) < len(values):
                        domains[cell] = new_values
                        changed = True

        return domains

    #explore assignments recursively and backtrack on failure
    def backtrack():
        domains = propagate_domains()

        if domains is None:
            return False

        if not domains:
            return is_magic_square(square)
    #choose variable with the fewest remaining values
        if use_mrv:
            (row, col), candidates = min(
                domains.items(),
                key=lambda item: len(item[1])
            )
        else:
            (row, col), candidates = next(
                iter(domains.items())
            )
    #order candidate values by how little they constrain the remaining variables
        if use_lcv:
            #evaluate how many possibilities remain after assigning num
            def lcv_score(num):

                square[row][col] = num
                used.add(num)
                future_domains = propagate_domains()
                square[row][col] = 0
                used.remove(num)

                if future_domains is None:
                    return -1

                return sum(
                    len(domain)
                    for domain in future_domains.values()
                )

            candidates = sorted(
                candidates,
                key=lcv_score,
                reverse=True
            )

        for num in candidates:
            square[row][col] = num
            used.add(num)

            if backtrack():
                return True

            square[row][col] = 0
            used.remove(num)

        return False


    for row, col in fixed_cells:
        if not valid_partial(row, col):
            return None

    if backtrack():
        return square

    return None

