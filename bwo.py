from fitness import fitness_func
import random
import matplotlib.pyplot as plt
from types_1 import Task, Fog, Network 
from typing import List
from file_functions import load_datas_from_file, save_datas_to_file, delete_files 

class BWO:

    pop : list[list[int]]
    pop_fitness : list[float]
    pop1: list[list[int]]
    pop1_fitness : list[float]
    pop2: list[list[int]]
    pop2_fitness : list[float]
    pop3: list[list[int]]
    pop3_fitness : list[float]
    prev_pop : list[list[int]] 
    best_widow : list[int]

    def __init__(self, pop_size: int, dim: int, max_epoch: int, reproduction_p: float, mutation_p: float, canni_p: float):
        self.pop_size = pop_size
        self.dim = dim
        self.max_epoch = max_epoch
        self.reproduction_p = reproduction_p
        self.mutation_p = mutation_p
        self.canni_p = canni_p
        self.fitness_cache = {}

    # CREATE POPULATION

    def create_population(self, min_val: int, max_val: int):
        self.pop = [[random.randint(min_val, max_val) for _ in range(self.dim)] for _ in range(self.pop_size)]

    # ADD TO POPULATION

    def add_to_population(self,data : list,data_to_add : list) -> tuple[list, list] :
        for solution in data_to_add:
            data.append(solution)
        return data, self.create_fitness_list(data)

    # CREATE FITNESS LIST

    def create_fitness_list(self, data: list) -> list:
        fitness_list = []
        for solution in data:
            key = tuple(solution)  # listeyi hashlenebilir hale getir
            if key in self.fitness_cache:
                fitness_list.append(self.fitness_cache[key])
            else:
                fit = fitness_func(solution)
                self.fitness_cache[key] = fit
                fitness_list.append(fit)
        return fitness_list


    # SORT DATAS 

    def sort_datas(self, datas : list) -> tuple[list,list] :
        fitness_list = self.create_fitness_list(datas) 
        sorted_solutions = sorted(zip(fitness_list, datas), key=lambda x: x[0])  
        sorted_fitness_list, sorted_datas = map(list, zip(*sorted_solutions)) 

        return sorted_datas, sorted_fitness_list 


    # SORT POPULATION

    def sort_population(self):
        sorted_solutions = sorted(zip(self.fitness_list, self.pop), key=lambda x: x[0])
        self.fitness_list, self.pop = zip(*sorted_solutions)
        self.fitness_list, self.pop = list(self.fitness_list), list(self.pop)

    def multiply_list_by_float(self, numbers, multiplier):
        return [num * multiplier for num in numbers]

    def get_cached_fitness(self, solution):
        key = tuple(solution)
        if key in self.fitness_cache:
            return self.fitness_cache[key]
        else:
            fit = fitness_func(solution)
            self.fitness_cache[key] = fit
            return fit

    # CREATE OFFSPRINGS

    def create_offspring(self):
        MAX_OFFSPRING = 300
        nr = int(len(self.pop1) * self.reproduction_p)
        children = []
        children_fitness = []   

        for i in range(nr):
            if len(children) >= MAX_OFFSPRING:
                break   

            parent1, parent2 = random.sample(self.pop1, 2)  

            for j in range(int(self.dim / 2)):
                if len(children) >= MAX_OFFSPRING:
                    break   

                child_1 = [random.choice([g1, g2]) for g1, g2 in zip(parent1, parent2)]
                child_2 = [random.choice([g1, g2]) for g1, g2 in zip(parent2, parent1)] 

                children.append(child_1)
                children.append(child_2)
                children_fitness.append(self.get_cached_fitness(child_1))
                children_fitness.append(self.get_cached_fitness(child_2))

            mother_parent = self.get_best_widow([parent1, parent2])
            father_parent = parent2 if mother_parent == parent1 else parent1
            self.pop1.remove(father_parent) 

        children, children_fitness = self.sort_datas(children)
        children, children_fitness = self.cannibalism(children, children_fitness)
        self.pop2.extend(children)
        self.pop2_fitness.extend(children_fitness)

    # CANNIBALISM ( REDUCE POPULATION ) 

    def cannibalism(self, data: list, fitness_list: list) -> tuple[list, list]:
        new_length = min(int(len(data) * self.canni_p), 300)
        data = data[:new_length]
        fitness_list = fitness_list[:new_length]
        return data, fitness_list

    def adapt_mutation_p(self, epoch):
        return max(0.05, 0.3 - 0.25 * (epoch / self.max_epoch))

    # APPLY MUTATION

    def mutate_pop(self):
        select_number = int(len(self.pop1) * self.mutation_p)
        selected_solutions = random.sample(self.pop1, select_number)

        mutated_solutions = []

        for solution in selected_solutions:
            if len(solution) > 1: 
                i, j = random.sample(range(len(solution)), 2)  
                solution[i], solution[j] = solution[j], solution[i]
            mutated_solutions.append(solution)
        
        self.pop3.extend(mutated_solutions)
        self.pop3_fitness = self.create_fitness_list(self.pop3)

    # GET THE BEST WIDOW

    def get_best_widow(self,datas : List[int]) :
        fitness_list = []
        for widow in datas:
            fitness_list.append(self.get_cached_fitness(widow))
        
        best_index = 0

        for i in range(len(datas)) :
            if(fitness_list[best_index] >= fitness_list[i]) : best_index = i

        return datas[best_index]

    def adapt_reproduction_p(self, epoch):
        # lineer azalsın mesela
        return max(0.3, 0.9 - 0.6 * (epoch / self.max_epoch))

    def adapt_canni_p(self, epoch):
        return max(0.3, 0.7 - 0.4 * (epoch / self.max_epoch))

    # START

    def selection(self):
        fogs : List[Fog] = load_datas_from_file("fogs.json")
        
        self.create_population(0, len(fogs) - 1)
    
        self.pop2 = []
        self.pop2_fitness = self.create_fitness_list(self.pop2)
        self.pop3 = []
        self.pop3_fitness = self.create_fitness_list(self.pop3)
    
        self.pop, self.pop_fitness = self.sort_datas(self.pop)
        
        global_best = self.pop_fitness[0]

        global_best_history = [global_best]

        for i in range(self.max_epoch):
            self.reproduction_p = self.adapt_reproduction_p(i)
            self.mutation_p = self.adapt_mutation_p(i)
            self.canni_p = self.adapt_canni_p(i)
            if(self.pop_fitness[0] < global_best) : 
                global_best = self.pop_fitness[0]
                global_best_history.append(global_best)
            print(f'Approach number : {i}, global best : {global_best}')
            
            nr = int(self.reproduction_p * len(self.pop))
            
            self.pop1 = self.pop[:nr]
            self.pop1_fitness = self.create_fitness_list(self.pop1)
  
            self.create_offspring()
            
            self.mutate_pop() 
            
            self.pop = [*self.pop2,*self.pop3]
            
            self.pop,self.pop_fitness = self.sort_datas(self.pop)
            self.pop = self.pop[:100]
            self.pop_fitness = self.create_fitness_list(self.pop)
            print(len(self.pop),len(self.pop1),len(self.pop2),len(self.pop3))
            self.pop2 = []
            self.pop2_fitness = []
            self.pop3 = []
            self.pop3_fitness = []
            

        plt.plot(range(len(global_best_history)), global_best_history, marker='o', linestyle='-')

        plt.title("Global Best History")
        plt.xlabel("Index (x)")
        plt.ylabel("Global Best (y)")

        plt.text(0, global_best_history[0] + 0.3, f"{round(global_best_history[0],2)}", fontsize=12, ha='right', va='bottom', color='red')
        plt.text(len(global_best_history) - 1, global_best_history[-1] + 0.3, f"{round(global_best_history[-1],2)}", fontsize=12, ha='left', va='top', color='red')

        plt.grid(True)
        plt.show()