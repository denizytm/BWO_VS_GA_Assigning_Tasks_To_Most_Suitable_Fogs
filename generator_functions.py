
import random
from typing import TypedDict, List
from types_1 import Task,Fog,Network

def generate_random_tasks(count: int) -> List[Task]:
    tasks = []
    for _ in range(count):
        task = Task(
            cpu_demand = round(random.uniform(10**3, 10**6), 2),
            memory_demand = round(random.uniform(10, 10 * 1024), 2),
            bandwidth_demand = random.randint(1, 1000),
            deadline = round(random.uniform(0.1, 5), 2),
            data_size = round(random.uniform(0.1, 500), 2),
            priority_level = random.randint(1, 10)
        )
        tasks.append(task)
    return tasks

def generate_random_fogs(count: int) -> List[Fog]:
    fogs = []
    for _ in range(count):
        fog = Fog(
            total_cpu_capacity = round(random.uniform(10**6, 10**9), 2),
            total_memory_capacity = round(random.uniform(1, 128), 2),
            total_bandwith_capacity = random.randint(100, 10000),
            idle_power_consumption = round(random.uniform(5, 50), 2),
            active_power_consumption = round(random.uniform(0.1, 2), 2),
            usage_cost = round(random.uniform(0.01, 0.5), 2)
        )
        fogs.append(fog)
    return fogs
    
def generate_random_network(row: int, column: int) -> List[List[Network]]:
    network = []  
    for _ in range(row):
        row_data = [] 
        for _ in range(column):
            connection = Network(
                available_bandwidth=round(random.uniform(100, 10000), 2),
                communication_latency=round(random.uniform(0.01, 0.2), 2)
            )
            row_data.append(connection)
        network.append(row_data)  
    return network