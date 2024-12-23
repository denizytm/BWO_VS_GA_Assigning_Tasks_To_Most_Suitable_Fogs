from typing import TypedDict

class Task(TypedDict):
    cpu_demand: float  
    memory_demand: float 
    bandwidth_demand: int
    deadline: float  
    data_size: float 
    priority_level: int 

class Fog(TypedDict):
    total_cpu_capacity: float  
    total_memory_capacity: float
    total_bandwith_capacity: float 
    idle_power_comsumption: float  
    active_power_consumption: float  
    usage_cost: float  

class Network(TypedDict):
    available_bandwidth: float  
    communication_latency: float 