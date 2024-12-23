import pandas as pd
from file_functions import load_datas_from_file, save_datas_to_file
from typing import List
from types_1 import Task, Fog, Network
from sklearn.preprocessing import StandardScaler
import numpy as np

tasks : List[Task] = load_datas_from_file("tasks.json")
fogs : List[Fog] = load_datas_from_file("fogs.json")
network : List[List[Network]] = load_datas_from_file("network.json")

E_values = []
L_values = []
U_values = []
C_values = []

def fitness_func(solution):

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
                ( (network[i][j]).get('communication_latency') + (task.get('cpu_demand') / fog.get('total_cpu_capacity')) + 1 ) 
            ):
                penalty += 1

        U /= len(fogs)

        E_values.append(E)
        L_values.append(L)
        U_values.append(U)
        C_values.append(C)
    
        # Minimum ve maksimumları hesapla
        E_min, E_max = min(E_values), max(E_values)
        L_min, L_max = min(L_values), max(L_values)
        U_min, U_max = min(U_values), max(U_values)
        C_min, C_max = min(C_values), max(C_values)
    
        # Normalizasyon
        E_normalized = (E - E_min) / (E_max - E_min) if E_max != E_min else 0.5
        L_normalized = (L - L_min) / (L_max - L_min) if L_max != L_min else 0.5
        U_normalized = (U - U_min) / (U_max - U_min) if U_max != U_min else 0.5
        C_normalized = (C - C_min) / (C_max - C_min) if C_max != C_min else 0.5

        """ print(E_normalized,L_normalized,U_normalized,C_normalized)  """

        return 1 * E_normalized + 1 * L_normalized - 1 * U_normalized + 1 * C_normalized + penalty