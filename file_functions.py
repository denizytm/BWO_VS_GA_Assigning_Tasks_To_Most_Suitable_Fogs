
import json
from typing import List
from types_1 import Task,Fog,Network

def save_datas_to_file(datas: List[Task] | List[Fog], filename: str) -> None:
    with open(filename, 'w') as file:
        json.dump(datas, file, indent=4)  

def load_datas_from_file(filename: str) -> List[Fog | Task | Network]:
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        raise

