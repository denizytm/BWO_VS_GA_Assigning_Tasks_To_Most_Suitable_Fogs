from fitness import fitness_func
import random
import matplotlib.pyplot as plt

class BWO:

    pop: list[list[int]]
    prev_pop : list[list[int]] 
    fitness_list : list[float]

    def __init__(self, pop_size: int, dim: int, max_epoch: int, cross_p: float, mutation_p: float, canni_p: float,nr : int):
        self.pop_size = pop_size
        self.dim = dim
        self.max_epoch = max_epoch
        self.cross_p = cross_p
        self.mutation_p = mutation_p
        self.canni_p = canni_p
        self.nr = nr

    # CREATE POPULATION

    def create_population(self, min_val: int, max_val: int):
        pop = [[random.randint(min_val, max_val) for _ in range(self.dim)] for _ in range(self.pop_size)]
        self.pop = pop

        self.create_fitness_list()

    # ADD TP POPULATION

    def add_to_population(self,value):
        for solution in value:
            self.pop.append(solution)
        self.create_fitness_list()

    # CREATE FITNESS LIST

    def create_fitness_list(self):
        fitness_list = []
        for solution in self.pop:
            fitness_list.append(fitness_func(solution))
        self.fitness_list = fitness_list

        self.sort_population()

    # SORT POPULATION

    def sort_population(self):
        sorted_solutions = sorted(zip(self.fitness_list, self.pop), key=lambda x: x[0])
        self.fitness_list, self.pop = zip(*sorted_solutions)
        self.fitness_list, self.pop = list(self.fitness_list), list(self.pop)

    # CREATE OFFSPRINGS

    def create_offspring(self) :
        if(self.nr <= 1) : raise ValueError("nr must be >= than 1")
        if(self.nr > len(self.pop)) : raise ValueError("nr must be <= than the population size")

        selected_solutions = self.pop[0:self.nr]
        a = self.cross_p

        for i in range(self.nr) :
            parent1, parent2 = random.sample(selected_solutions, 2)

            y1 : list[int] = []
            y2 : list[int] = []

            for i in range(self.dim):
                offspring_1, offspring_2 = ( a * parent1[i] + (1-a) * parent2[i] ), ( a * parent2[i] + (1-a) * parent1[i] ) 

                y1.append(round(offspring_1))
                y2.append(round(offspring_2))

            self.pop.extend([y1,y2])
            self.fitness_list.extend([fitness_func(y1),fitness_func(y2)])

        self.sort_population()  
 
    # REDUCE POPULATION ( CANNIBALISM ) 

    def reduce_population(self):
        new_length = int(len(self.pop) * self.canni_p)
        self.pop = self.pop[:new_length]
        self.fitness_list = self.fitness_list[:new_length]

    # APPLY MUTATION

    def mutate_pop(self):
        select_number = int(len(self.pop) * self.mutation_p)
        selected_solutions = random.sample(self.pop, select_number)

        mutated_solutions = []

        for solution in selected_solutions:
            if len(solution) > 1: 
                i, j = random.sample(range(len(solution)), 2)  
                solution[i], solution[j] = solution[j], solution[i]
            mutated_solutions.append(solution)
        
        self.add_to_population(mutated_solutions)

    # START

    def selection(self):
        self.create_population(0,9)

        first_length = len(self.pop)

        global_best = self.fitness_list[0]

        global_best_history = [global_best]

        for i in range(self.max_epoch):
            if(self.fitness_list[0] < global_best) : 
                global_best = self.fitness_list[0]
                global_best_history.append(global_best)
            print(f'Approach number : {i}, global best : {global_best}')
            print(len(self.pop))
            self.create_offspring()
            self.prev_pop = self.pop
            self.reduce_population()
            self.mutate_pop()
            if(len(self.pop) > 150) : self.reduce_population()
            if( first_length * 0.45 > len(self.pop) ) :
                pop = [[random.randint(0, 9) for _ in range(self.dim)] for _ in range(self.pop_size)]
                self.add_to_population(pop)

        plt.plot(range(len(global_best_history)), global_best_history, marker='o', linestyle='-')

        plt.title("Global Best History")
        plt.xlabel("Index (x)")
        plt.ylabel("Global Best (y)")

        plt.text(0, global_best_history[0] + 0.3, f"{round(global_best_history[0],2)}", fontsize=12, ha='right', va='bottom', color='red')
        plt.text(len(global_best_history) - 1, global_best_history[-1] + 0.3, f"{round(global_best_history[-1],2)}", fontsize=12, ha='left', va='top', color='red')

        plt.grid(True)
        plt.show()
