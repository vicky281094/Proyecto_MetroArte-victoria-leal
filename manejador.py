import requests 
from PIL import Image

def cargar_nacionalidades():    
    nacionalidades = requests.get('https://drive.google.com/uc?id=1tJEU6_VEeO6xFH8fssSfkw4M8MaN6U5A&export=download')
    with open('nacionalidades.csv', 'wb') as f:
            f.write(nacionalidades.content)
        
def manejar_nacionalidades():
    with open('nacionalidades.csv', 'r') as f:
        nacionalidades = f.readlines()
        naciones = []
        for linea in nacionalidades:
            valor = linea.strip()
            naciones.append(valor)
        return naciones

def  cargar_obras():
    url = 'https://collectionapi.metmuseum.org/public/collection/v1/objects?departmentIds=1'
    obras = requests.get(url)
    obras = obras.json()
    obras = obras['objectIDs']
    obras = obras
    print(obras)
    print(f'Cantidad de obras: {len(obras)}')
        
    
    
        
        
    
    

def cargar_departaments():
    departamentos = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/departments')
    departamentos = departamentos.json()
    departamentos = departamentos['departments']
    for departamento in departamentos:
        print(departamento)

cargar_obras()