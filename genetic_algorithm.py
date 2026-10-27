
import random
from magic_square import magic_constant


def create_population(n, population_size, fixed_cells=None, seed=None):
    if type(n) is not int or n < 1:
        raise ValueError("n must be a positive integer")

    if type(population_size) is not int or population_size < 1:
        raise ValueError("Population size must be positive")

    if fixed_cells is None:
        fixed_cells = {}

    used = set()

    for position, num in fixed_cells.items():
        if (not isinstance(position, tuple) or len(position) != 2
            or any(type(x) is not int for x in position)):
            raise ValueError("Invalid cell position")

        row, col = position

        if not (0 <= row < n and 0 <= col < n):
            raise ValueError("Cell position outside the square")

        if type(num) is not int or not (1 <= num <= n*n) or num in used:
            raise ValueError("Invalid fixed value")

        used.add(num)

    available = [
        num for num in range(1, n*n+1)
        if num not in used
    ]

    rng = random.Random(seed)
    population = []

    for _ in range(population_size):
        individual = available[:]
        rng.shuffle(individual)
        population.append(individual)

    return population


def decode_individual(individual, n, fixed_cells=None):
    if fixed_cells is None:
        fixed_cells = {}

    expected = set(range(1, n*n+1)) - set(fixed_cells.values())

    if len(individual) != len(expected) or set(individual) != expected:
        raise ValueError("Invalid individual")

    square = [[0]*n for _ in range(n)]

    for (row, col), num in fixed_cells.items():
        square[row][col] = num

    values = iter(individual)

    for row in range(n):
        for col in range(n):
            if square[row][col] == 0:
                square[row][col] = next(values)

    return square


def fitness(individual, n, fixed_cells=None):
    square = decode_individual(individual, n, fixed_cells)
    target = magic_constant(n)

    error = 0

    for row in square:
        error += abs(sum(row) - target)

    for col in range(n):
        error += abs(
            sum(square[row][col] for row in range(n)) - target
        )

    error += abs(
        sum(square[i][i] for i in range(n)) - target
    )

    error += abs(
        sum(square[i][n-1-i] for i in range(n)) - target
    )

    return 1 / (1 + error)



def select_parent(population, n, fixed_cells=None, rng=None, weights=None):
    if rng is None:
        rng = random.Random()

    if not population:
        raise ValueError("Population cannot be empty")

    if weights is None:
        weights = [
            fitness(individual, n, fixed_cells)
            for individual in population
        ]

    return rng.choices(
        population,
        weights=weights,
        k=1
    )[0]



def order_crossover(parent1, parent2, rng=None):
    if rng is None:
        rng = random.Random()

    if (len(parent1) != len(parent2)
        or set(parent1) != set(parent2)
        or len(set(parent1)) != len(parent1)):
        raise ValueError("Parents must be permutations of the same values")

    size = len(parent1)

    if size < 2:
        return parent1[:]

    start, end = sorted(rng.sample(range(size), 2))

    child = [None]*size

    child[start:end+1] = parent1[start:end+1]

    index = (end+1) % size

    for offset in range(size):
        gene = parent2[(end+1+offset) % size]

        if gene not in child:
            child[index] = gene
            index = (index+1) % size

    return child


def swap_mutation(individual, mutation_rate=0.1, rng=None):
    if rng is None:
        rng = random.Random()

    if not 0 <= mutation_rate <= 1:
        raise ValueError("Mutation rate must be between 0 and 1")

    mutated = individual[:]

    if len(mutated) < 2:
        return mutated

    if rng.random() < mutation_rate:
        i, j = rng.sample(range(len(mutated)), 2)

        mutated[i], mutated[j] = mutated[j], mutated[i]

    return mutated



def solve_genetic_algorithm(n, fixed_cells=None,
                            population_size=40,
                            max_generations=1000,
                            mutation_rate=0.2,
                            seed=None):

    if type(population_size) is not int or population_size < 2:
        raise ValueError("Population size must be at least 2")

    if type(max_generations) is not int or max_generations < 0:
        raise ValueError("Invalid maximum generations")

    if not 0 <= mutation_rate <= 1:
        raise ValueError("Invalid mutation rate")

    if fixed_cells is None:
        fixed_cells = {}

    rng = random.Random(seed)

    population = create_population(
        n, population_size, fixed_cells, seed
    )

    for generation in range(max_generations+1):

        weights = [
            fitness(individual, n, fixed_cells)
            for individual in population
        ]

        best_index = max(
            range(len(population)),
            key=lambda i: weights[i]
        )

        if weights[best_index] == 1.0:
            return decode_individual(
                population[best_index], n, fixed_cells
            )

        if generation == max_generations:
            break

        new_population = [population[best_index][:]]

        while len(new_population) < population_size:

            parent1 = select_parent(
                population, n, fixed_cells, rng, weights
            )

            parent2 = select_parent(
                population, n, fixed_cells, rng, weights
            )

            child = order_crossover(parent1, parent2, rng)

            child = swap_mutation(
                child, mutation_rate, rng
            )

            new_population.append(child)

        population = new_population

    return None



if __name__ == "__main__":
    from magic_square import print_square, is_magic_square

    fixed_cells = {
        (0, 0): 8,
        (1, 1): 5,
        (2, 2): 2
    }

    square = solve_genetic_algorithm(
        n=3,
        fixed_cells=fixed_cells,
        population_size=40,
        max_generations=1000,
        mutation_rate=0.2,
        seed=42
    )

    if square is not None:
        print("=== GENETIC ALGORITHM ===")
        print_square(square)
        print("Valid:", is_magic_square(square))

        preserved = all(
            square[row][col] == num
            for (row, col), num in fixed_cells.items()
        )

        print("Fixed cells preserved:", preserved)
    else:
        print("No valid solution found")
