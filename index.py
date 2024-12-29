
from mealpy import IntegerVar, GA
import numpy as np
from typing import List
from types_1 import Task, Fog, Network 

from generator_functions import (
    generate_random_fogs,
    generate_random_network,
    generate_random_tasks
)

from file_functions import load_datas_from_file, save_datas_to_file 

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

except FileNotFoundError:
    tasks = generate_random_tasks(10)
    save_datas_to_file(tasks, "tasks.json")
    print(f"{len(tasks)} tasks created and saved.")
    fogs = generate_random_fogs(3)
    save_datas_to_file(fogs, "fogs.json")
    print(f"{len(fogs)} fogs created and saved.")
    network = generate_random_network(len(tasks),len(fogs))
    save_datas_to_file(network, "network.json")
    print(f"{len(tasks)} X {len(fogs)} network created and saved.")
    print("run index again to use the fitness function")