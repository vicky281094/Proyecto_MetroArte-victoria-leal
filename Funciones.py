
import json

with open('departamentos.csv','r', encoding='utf-8') as f:
    lector = json.load(f)
    
    print(lector)
    
    