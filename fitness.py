import pandas as pd
from file_functions import load_datas_from_file, save_datas_to_file
from typing import List
from types_1 import Task, Fog, Network
from sklearn.preprocessing import StandardScaler
import numpy as np
import math

tasks : List[Task] = load_datas_from_file("tasks.json")
fogs : List[Fog] = load_datas_from_file("fogs.json")
network : List[List[Network]] = load_datas_from_file("network.json")

E_values = []
L_values = []
U_values = []
C_values = []

def fitness_func(solution):
        
        solution = [math.floor(data) for data in solution]

        penalty = 0

        E = 0
        L = 0
        U = 0
        C = 0

        for fog in fogs:
            E += fog.get('idle_power_consumption') 

        for _ in range(len(solution)):
            i = int(_)
            j = int(solution[i])
            task : Task = tasks[i]
            fog : Fog = fogs[j]

            E += task.get('cpu_demand') * fog.get('active_power_consumption')
            L += (network[i][j]).get('communication_latency') + (task.get('cpu_demand') / fog.get('total_cpu_capacity')) 
            U += ( 
                    (task.get('cpu_demand') / fog.get('total_cpu_capacity')) 
                    + 
                    (task.get('memory_demand') / fog.get('total_memory_capacity')) 
                    + 
                    (task.get('bandwidth_demand') / fog.get('total_bandwith_capacity')) 
                )
            C +=  (
                task.get('cpu_demand') 
                * 
                fog.get('usage_cost') 
                + 
                ( ( task.get('data_size') / (network[i][j]).get('available_bandwidth') ) * fog.get('usage_cost') )
            )

            if(task.get('cpu_demand') > fog.get('total_cpu_capacity')):
                penalty += 1
            if(task.get('memory_demand') > fog.get('total_memory_capacity')):
                penalty += 1
            if(task.get('bandwidth_demand') > fog.get('total_bandwith_capacity')):
                penalty += 1

            if(
                task.get('bandwidth_demand') >(network[i][j]).get('available_bandwidth')
            ):
                penalty += 1

            if(
                task.get('deadline') 
                < 
                ( (network[i][j]).get('communication_latency') + (task.get('cpu_demand') / fog.get('total_cpu_capacity')) ) 
            ):
                penalty += 1

        U /= len(fogs)
        
        return 1 * E + 1 * L - 1 * U + 1 * C + penalty