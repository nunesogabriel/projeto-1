import random
import time


def extract_data(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    n = int(lines[0].strip())
    capacity = int(lines[-1].strip())

    value, weight = [], []
    for line in lines[1:-1]:
        numbers = [int(x) for x in line.strip().split()]
        value.append(numbers[1])
        weight.append(numbers[2])

    return n, value, weight, capacity


def get_fitness(individual, weights, values, capacity):
    value = 0
    weight = 0
    for i in range(len(individual)):
        if (individual[i] != 0 and values[i] != 0):
            value += individual[i] * values[i]
            weight += individual[i] * weights[i]
    if weight > capacity:
        return 0
    else:
        return value


def select_parents(population, fitness):
    if (sum(fitness) == 0):
        fitness = [1 for _ in fitness]
    return random.choices(population, weights=fitness, k=2)


def cross_parents(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2


def mutation(individual, rate):
    for i in range(len(individual)):
        if random.random() < rate:
            individual[i] = 1 - individual[i]


def start_population(n, number_individuals, weights, capacity):
    population = []
    for _ in range(number_individuals):
        individual = [0 for _ in range(n)]
        current_weight = 0
        for i in random.sample(range(n), n):
            if current_weight + weights[i] <= capacity:
                individual[i] = random.randint(0, 1)
                current_weight += individual[i] * weights[i]
        population.append(individual)
    return population

def main(file_path, iterator):
    n, value, weight, capacity = extract_data(file_path)

    number_individuals = 10
    number_generations = 100
    rate_mutation = 0.05
    population = start_population(n, number_individuals, weight, capacity)

    best_individual = None
    best_fitness = -1

    for _ in range(number_generations):
        fitness = [get_fitness(ind, weight, value, capacity) for ind in population]

        best_individual_tmp = max(population, key=lambda x: get_fitness(x, weight, value, capacity))
        best_fitness_tmp = get_fitness(best_individual_tmp, weight, value, capacity)

        if best_fitness_tmp > best_fitness:
            best_fitness = best_fitness_tmp
            best_individual = best_individual_tmp.copy()

        new_population = []
        while len(new_population) < number_individuals - 1:
            parent1, parent2 = select_parents(population, fitness)
            child1, child2 = cross_parents(parent1, parent2)
            mutation(child1, rate_mutation)
            mutation(child2, rate_mutation)
            new_population.extend([child1, child2])

        new_population.append(best_individual)

        population = new_population
        output_line = f"Instancia {iterator} : {best_fitness}\n"

    with open("output/genetico.out", "a+") as output_file:
            output_file.write(output_line)

if __name__ == "__main__":
    print('Begin')
    with open(f"output/output_time_ag.txt", 'a+') as file: 
        for iterator in range(1, 17):
            start_time = time.time()
            file_path = f"input/input{iterator}.in"
            main(file_path, iterator)
            execution_time = time.time() - start_time
            file.write(str(execution_time) + '\n')
    print('End')