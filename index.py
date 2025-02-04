
from mealpy import IntegerVar, GA
import numpy as np
from typing import List
from types_1 import Task, Fog, Network 

from generator_functions import (
    generate_random_fogs,
    generate_random_network,
    generate_random_tasks
)

from file_functions import load_datas_from_file, save_datas_to_file, delete_files 


try:

    tasks : List[Task] = load_datas_from_file("tasks.json")
    fogs : List[Fog] = load_datas_from_file("fogs.json")
    network : List[List[Network]] = load_datas_from_file("network.json")

    from fitness import fitness_func 

    print(f"Datas has been loaded type") 

    problem_dict = {
        "obj_func": fitness_func,
        "bounds": IntegerVar(lb=[0, ] * len(tasks), ub=[len(fogs) - 1, ] * len(tasks)),
        "minmax": "min",
    }

    optimizer = GA.BaseGA(epoch=100, pop_size=100, pc=0.9, pm=0.2)
    optimizer.solve(problem_dict)
    print(optimizer.g_best.solution)
    print(optimizer.g_best.target.fitness)   

    import matplotlib.pyplot as plt

    global_best_values = optimizer.history.list_global_best_fit
    current_best_values = optimizer.history.list_current_best_fit

    # X
    epochs = list(range(1, len(global_best_values) + 1))

    plt.figure(figsize=(10, 5))

    plt.plot(epochs, global_best_values, marker='o', linestyle='-', color='b', label="Global Best Fitness") 

    """ plt.plot(epochs, current_best_values, marker='s', linestyle='--', color='r', label="Current Best Fitness") """

    plt.xlabel("Epoch")
    plt.ylabel("Fitness Değeri")
    plt.title("Global Best Fitness")
    plt.legend()
    plt.grid()

    plt.show()

except FileNotFoundError:
    tasks = generate_random_tasks(150)
    save_datas_to_file(tasks, "tasks.json")
    print(f"{len(tasks)} tasks created and saved.")
    fogs = generate_random_fogs(10)
    save_datas_to_file(fogs, "fogs.json")
    print(f"{len(fogs)} fogs created and saved.")
    network = generate_random_network(len(tasks),len(fogs))
    save_datas_to_file(network, "network.json")
    print(f"{len(tasks)} X {len(fogs)} network created and saved.")
    print("run index again to use the fitness function")