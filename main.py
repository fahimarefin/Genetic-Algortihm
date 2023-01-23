import random


def random_chromosome(size):
    return [random.randint(0, 64) for i in range(nq)]


def fitness(chromosome):
    horizontal_collisions = sum([chromosome.count(queen) - 1 for queen in chromosome]) / 2

    diagonal_collisions = 0

    n = len(chromosome)

    left_diagonal = [0] * 2 * n
    right_diagonal = [0] * 2 * n
    for i in range(n):
        left_diagonal[i + (chromosome[i] % 8) - 1] += 1
        right_diagonal[len(chromosome) - i + (chromosome[i] % 8) - 2] += 1

    for i in range(2 * n - 1):
        counter = 0
        if left_diagonal[i] > 1:
            counter += left_diagonal[i] - 1
        if right_diagonal[i] > 1:
            counter += right_diagonal[i] - 1
        diagonal_collisions += counter / (n - abs(i - n + 1))

    return int(maxFitness - (horizontal_collisions + diagonal_collisions))  # 28-(2+3)=23


def probability(chromosome, fitness):
    return fitness(chromosome) / maxFitness


def random_pick(population, probabilities):
    populationWithProbabilty = zip(population, probabilities)
    total = sum(w for c, w in populationWithProbabilty)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(population, probabilities):
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"


def reproduce(x, y):
    n = len(x)
    c = random.randint(0, n - 1)
    return x[0:c] + y[c:n]


def mutate(x):
    n = len(x)
    c = random.randint(0, n - 1)
    m = random.randint(1, n)
    x[c] = m
    return x


def genetic_queen(population, fitness):
    mutation_probability = 0.03
    new_population = []
    probabilities = [probability(n, fitness) for n in population]
    for i in range(len(population)):
        x = random_pick(population, probabilities)
        y = random_pick(population, probabilities)
        child = reproduce(x, y)
        if random.random() < mutation_probability:
            child = mutate(child)

        new_population.append(child)
        if fitness(child) == maxFitness: break
    return new_population


def return_currenbest(chrom):
    max = 0
    returnchorm = 0
    for i in chrom:
        hold = fitness(i)
        if hold > max:
            max = hold
            returnchorm = i

    return returnchorm


if __name__ == "__main__":
    nq = int(8)
    maxFitness = (nq * (nq - 1)) / 2
    population = [random_chromosome(nq) for _ in range(6)]

    generation = 1

    for i in range(0, 100000):
        population = genetic_queen(population, fitness)
        if i == 0:
            for k in range(len(population)):
                print("Sample No.", k, "=", population[k])
                print("Fitness:", fitness(population[k]))

        if i % 10000 == 0 and i!=0:
            print("Iteration:", i)
            print(return_currenbest(population))
            print("Fitness = {}".format(max([fitness(n) for n in population])))
