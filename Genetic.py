import random

def create_individual(individual_size):
    return [random.uniform(-1, 1) for _ in range(individual_size)]

def generate_population(individual_size, population_size):
    return [create_individual(individual_size) for _ in range(population_size)]

def genetic_algorithm(individual_size, population_size, fitness_function, target_fitness, generations, elite_rate=0.2, mutation_rate=0.05):
    population = generate_population(individual_size, population_size)
    best_individual = None
    best_fitness = float('-inf')
    elite_count = max(1, int(elite_rate * population_size))

    for generation in range(generations):
        # Avalia o fitness de cada ind e ordena do melhor para o pior
        scored_population = [(ind, fitness_function(ind, seed=generation)) for ind in population]
        scored_population.sort(key=lambda x: x[1], reverse=True)

        if scored_population[0][1] > best_fitness:
            # atualiza o melhor indivíduo
            best_individual = scored_population[0]
            best_fitness = best_individual[1]

        if best_fitness >= target_fitness:
            break

        # Elitismo - nova população com os melhores ind
        new_population = [ind for ind, _ in scored_population[:elite_count]]

        while len(new_population) < population_size:
            parent1 = random.choice(scored_population[:elite_count])[0]
            parent2 = random.choice(scored_population[:elite_count])[0]

            # Crossover - cruza dois dos melhores ind
            point = random.randint(1, individual_size - 1)
            child = parent1[:point] + parent2[point:]

            # Mutação - aplica mudanças aleatórias
            for i in  range(individual_size):
                if random.random() < mutation_rate:   # se número for menor da chance, ocorre mutação no gene
                    child[i] += random.uniform(-0.1, 0.1)     # soma um valor entre -0.1 e +0.1 ao gene

            new_population.append(child)

        population = new_population

    return best_individual  #(individual, fitness)