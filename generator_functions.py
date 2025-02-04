
import random
from typing import TypedDict, List
from types_1 import Task,Fog,Network

def normalize(x,xMin,xMax):
    return (
         (  x - xMin ) / ( xMax - xMin )
    )

def generate_random_tasks(count: int) -> List[Task]:
    tasks = []
    for _ in range(count):
        task = Task(
            cpu_demand = normalize(round(random.uniform(10**3, 10**6), 2),10**3,10**6),
            memory_demand = normalize(round(random.uniform(10, 10000), 2),(10),10000),
            bandwidth_demand = normalize(random.randint(1, 1000),1,1000),
            deadline = normalize(round(random.uniform(0.1, 5), 2),0.1,5),
            data_size =  normalize(round(random.uniform(0.1, 500), 2),0.1,500),
            priority_level = normalize(random.randint(1, 10),1,10)
        )
        tasks.append(task)
    return tasks

def generate_random_fogs(count: int) -> List[Fog]:
    fogs = []
    for _ in range(count):
        fog = Fog(
            total_cpu_capacity = normalize(round(random.uniform(10**6, 10**9), 2),10**6,10**9),
            total_memory_capacity = normalize(round(random.uniform(1, 128), 2),1,128),
            total_bandwith_capacity = normalize(random.randint(100, 10000),100, 10000),
            idle_power_consumption = normalize(round(random.uniform(5, 50), 2),5,50),
            active_power_consumption = normalize(round(random.uniform(0.1, 2), 2),0.1,2),
            usage_cost = normalize(round(random.uniform(0.01, 0.5), 2),0.01,0.5)
        )
        fogs.append(fog)
    return fogs
    
def generate_random_network(row: int, column: int) -> List[List[Network]]:
    network = []  
    for _ in range(row):
        row_data = [] 
        for _ in range(column):
            connection = Network(
                available_bandwidth= normalize(round(random.uniform(100, 10000), 2),100,10000),
                communication_latency= normalize(round(random.uniform(0.01, 0.2), 2),0.01,0.2)
            )
            row_data.append(connection)
        network.append(row_data)  
    return network