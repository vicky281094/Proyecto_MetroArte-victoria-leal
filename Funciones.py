# Se importa librería para manejar los datos disponibles
import csv
import requests
from Objetos import Autor,Departamento, Museo

# Se define la lista
departamentos = [] 
nacionalidades = []
artistas = []

#Esta función nos dan los datos contenidos en los csv de lo último que se obtuvo al usar la función manejador
def lista_renovada():

    with open('listas/departamentos.csv', mode='r', encoding='utf-8') as f:
        # Usamos DictReader, que usa los encabezados como claves de diccionario
        lector_csv = csv.DictReader(f)
        
        # Recorremos cada fila del archivo CSV
        for fila in lector_csv:
            # Cada 'fila' ya es un diccionario gracias a DictReader
            departamento = Departamento(fila['departmentId'],fila['displayName'])
            
            departamentos.append(departamento)
            
    
    with open('listas/artistas.csv', mode='r', encoding='utf-8') as f:
    # Usamos DictReader, que usa los encabezados como claves de diccionario
        lector_csv = csv.DictReader(f)
        
        # Recorremos cada fila del archivo CSV
        for fila in lector_csv:
            # Creamos una instancia de la clase Departamento
            # usando los valores de cada fila.
            artista = Autor(fila['artista'], fila['nacionalidad'], fila['nacimiento'],fila['muerte'])
            
            if artista.nombre == 'Desconocido':
                print("Se elimino el desconocido")
            # Añadimos el objeto a nuestra lista
            else:
                artistas.append(artista)

    

    with open('listas/nacionalidades.csv', mode='r', encoding='utf-8') as f:
            lector_csv = csv.reader(f)
            for fila in lector_csv:
                # 'fila' es una lista de strings, por ejemplo, ['American']
                # Si la fila no está vacía, añadimos el primer elemento a la lista
                if fila:
                    nacionalidades.append(fila[0])
    museo = Museo(departamentos,artistas,nacionalidades)
    return museo
    
    
            

# Esta función nos ofrece los datos que se ofrece en la API respecto a departamentos y el csv que se tiene en Google Drive
def listas_determinada():
    nacionalidades = []
    departamentos = []
    url_nacionalidades = "https://drive.google.com/uc?export=download&id=1tJEU6_VEeO6xFH8fssSfkw4M8MaN6U5A"
    
    try:
        response = requests.get(url_nacionalidades)
        response.raise_for_status() # Lanza un error si hay un problema de conexión

        # Leemos el contenido como texto en lugar de JSON
        texto_nacionalidades = response.text
        
        # Procesamos cada línea del texto para crear una lista de nacionalidades
        nacionalidades = texto_nacionalidades.strip().split('\n')
        
        # Eliminamos espacios en blanco extra de cada nacionalidad
        nacionalidades = [n.strip() for n in nacionalidades if n.strip()]
        nacionalidades = nacionalidades[1:]
        
        print("Datos de nacionalidades cargados exitosamente.")
        
        

    except requests.exceptions.RequestException as e:
        print(f"Error al descargar o procesar el archivo: {e}")
        

    url_departamentos = "https://collectionapi.metmuseum.org/public/collection/v1/departments"
    try:
        response = requests.get(url_departamentos)
        response.raise_for_status()
        departamentos = response.json()
        print("Datos de departamentos cargados exitosamente.")
        departamentos_lista = departamentos['departments']
        departamentos = []
        
        for dep in departamentos_lista:
            departamento = Departamento(dep['departmentId'],dep['displayName'])
            departamentos.append(departamento)
        
        
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar o procesar el archivo: {e}")
    
    museo = Museo(departamentos,artistas,nacionalidades)
    
    return museo 
        
    
# Llamamos a la función corregida
listas_determinada()