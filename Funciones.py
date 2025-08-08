# Se importa librería para manejar los datos disponibles
import csv
import requests
import subprocess
import time
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
        print(f"\n\n Error al descargar o procesar el archivo: {e} \n\n")
        

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
        print(f"\n\n Error al descargar o procesar el archivo: {e} \n\n")
    
    museo = Museo(departamentos,artistas,nacionalidades)
    
    return museo 
        
    
        
def reconexion():
    nombre_interfaz = "Wi-Fi"
    print(f"Deshabilitando la conexión: {nombre_interfaz}")
    try:
        # Comando para deshabilitar la interfaz de red
        subprocess.run(
            ['netsh', 'interface', 'set', 'interface', nombre_interfaz, 'admin=disable'],
            check=True,
            shell=True
        )
        print("Conexión deshabilitada.")
        
        # Pausa para dar tiempo a que la conexión se apague
        time.sleep(5)
        
        print(f"Habilitando la conexión: {nombre_interfaz}")
        # Comando para habilitar la interfaz de red
        subprocess.run(
            ['netsh', 'interface', 'set', 'interface', nombre_interfaz, 'admin=enable'],
            check=True,
            shell=True
        )
        print("Conexión habilitada.")
        time.sleep(15)

    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")
        print("\n\nAsegúrate de que el script se ejecuta como Administrador.\n\n")
    except FileNotFoundError:
        print("\n\nEl comando 'netsh' no se encontró. Verifica tu instalación de Windows.\n\n")


def busqueda_id(tipo, caracteristica):
    
    
    if tipo == "nacionalidad":
        url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?q={caracteristica}"
        
        
    elif tipo == "departamento":
        id = caracteristica.id
        q = caracteristica.nombre
        url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?departmentId={id}&q={q}"
        
        
    else:
        url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?artistOrCulture=true&q={caracteristica}"
        
        
    
    response = requests.get(url)        
    response = response.json()
    
    return response
            
    

def mostrar(response,tipo):
    total = response['total']
    Ids = response['objectIDs']
    while True:
        if total <= 30:
            num = 1
            conjunto =  []
            for obra in Ids:
                max_intentos = 10
                intentos = 0
                while intentos < max_intentos:
                    obra = str(obra)
                    url = f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{obra}'
                    obra_detalle = requests.get(url)
                    obra_detalle = obra_detalle.json()

                    # A fin de que  funcione todo correctamente, se dará 3 intentos para corregir las excepciones, en caso de no poderse se culminará el 
                    # proceso hasta lo obtenido
                    
                    
                    try:
                        
                        if 'objectID' in obra_detalle:
                            if not obra_detalle['objectID']:
                                obra_id = 'Desconocido'
                            else:
                                obra_id = obra_detalle['objectID'] 
                        
                        # Se realiza verficación de la data disponible en el campo que contiene el título
                        if 'title' in obra_detalle:
                            if not obra_detalle['title']:
                                titulo = 'Desconocido'
                            else:
                                titulo = obra_detalle['title'] 
                                
                        #  Se elimina datos repetidos y se ordena de a hasta la z
                        if 'artistDisplayName' in obra_detalle:
                            if not obra_detalle['artistDisplayName']:
                                nombre = 'Desconocido'
                            else:
                                nombre = obra_detalle['artistDisplayName']
                        
                        print(f"{num}.- ID: {obra_id}, Obra: {titulo}, Autor: {nombre} ")
                        nuevo = f"{num}.- ID: {obra_id}, Obra: {titulo}, Autor: {nombre} "
                        conjunto.append(nuevo)
                    
                        intentos = 11
                        num += 1
                        
                        
                            
                                
                            
                    except   (ConnectionError, TimeoutError) as errh:
                        # Se presenta un error se llama la función  reconexión de modo que reinicie la conexión de la computadora si encuentra conectada en 
                        # wifi
                        intentos +=1
                        reconexion()
                        time.sleep(10)
                        intentos +=1 
                        print("Se presentó problemas de conexión")
                        print(f"\n\n Intento: {intentos}\n\n")
                                                            
                    except requests.exceptions.HTTPError as errh:
                        # Esta es la excepción cuando no se obtiene datos de la API
                        # Se hace un tiempo de espera de un minuto con el fin de dar oportunidad de que cargue y pueda funcionar el servidor
                        intentos +=1
                        print(f"Error HTTP al obtener la obra de ID: {obra_id}: {errh}")
                        reconexion()
                        time.sleep(10)
                        intentos +=1 
                        print(f"\n\n Intento: {intentos}\n\n")
                    
                    except requests.exceptions.JSONDecodeError as e:
                        print(f"Error de formato JSON para la obra de ID: {obra_id}: {e}")
                        time.sleep(10)
                        intentos +=1 
                        print(f"\n\n Intento: {intentos}\n\n")
                        
            while True: 
                opcion = int(input(f"""
                        Indique la opción que desea tomar:
                        
                        1.- Seleccionar ID :
                        2.- Cambiar {tipo}
                        3.- Salir al menú principal
                        
                        Indicar opción : """).strip())
                
                try:
                    if opcion == 1:
                        while True:
                            print("")
                            for obra in conjunto:
                                print(obra)
                            selec_id = int(input(" \n\nSeleccionar el número que acompaña la información de la obra: "))
                            selec_id -= 1
                            try:
                                id = Ids[selec_id]
                                salida = True
                                return id, salida
                            except ValueError: 
                                print("\n\nSelecciona el valor de las obras disponibles\n\n")
                            except IndexError:
                                print("\n\nIngresaste un número fuera del rango de obras disponibles\n\n")
                    elif opcion == 2:
                        id =  " No seleccionado "
                        salida = False
                        return id, salida
                    elif opcion == 3:
                        id =  " No seleccionado "
                        salida = True
                        return id, salida
                    else: 
                        print("\n No ingresaste ninguna de las opciones \n")
                except ValueError:
                    print("\n\nDebe ingresar número en función a lo indicado\n\n")
            
            
        else: 
            while True:
                print(f""" 
                      Se presenta {total} de obras, por lo que presentará un número limitado de obras, para ello se requiere:
                         - Indicar la cantidad de obras que quieres mostrar, el máximo son 50 obras para presentarse, el mínimo es 1
                         - Indicar a partir de que valor se desea buscar, su posción debes indicarlo desde el 1 hasta {total}
                      """)
                rango = int(input("Indicar la cantidad de valores: ").strip())
                pri_obra = int(input("Indicar la poscición del primer valor: ").strip())
                
                try:
                    
                    conjunto = []
                    id_obra = []
                    
                    if rango <= 50 and 1<= pri_obra and pri_obra <= total and rango > 0: 
                        indice = pri_obra - 1
                        num = 1
                        while num <= rango  and indice < total:
                            max_intentos = 10
                            intentos = 0
                            
                            while intentos < max_intentos:
                                

                                # A fin de que  funcione todo correctamente, se dará 10 intentos para corregir las excepciones, en caso de no poderse se culminará el 
                                # proceso hasta lo obtenido
                                
                                
                                try:
                                    
                                    id = str(Ids[indice])
                                    url = f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{id}'
                                    obra_detalle = requests.get(url)
                                    obra_detalle = obra_detalle.json()
                                    
                                    if 'objectID' in obra_detalle:
                                        if not obra_detalle['objectID']:
                                            obra_id = 'Desconocido'
                                        else:
                                            obra_id = obra_detalle['objectID'] 
                                    
                                    id_obra.append(obra_id)
                                    
                                    # Se realiza verficación de la data disponible en el campo que contiene el título
                                    if 'title' in obra_detalle:
                                        if not obra_detalle['title']:
                                            titulo = 'Desconocido'
                                        else:
                                            titulo = obra_detalle['title'] 
                                            
                                    #  Se elimina datos repetidos y se ordena de a hasta la z
                                    if 'artistDisplayName' in obra_detalle:
                                        if not obra_detalle['artistDisplayName']:
                                            nombre = 'Desconocido'
                                        else:
                                            nombre = obra_detalle['artistDisplayName']
                                    
                                    print(f"{num}.- ID: {obra_id}, Obra: {titulo}, Autor: {nombre} ")
                                    obra = f"{num}.- ID: {obra_id}, Obra: {titulo}, Autor: {nombre} "
                                    conjunto.append(obra)
                                    intentos = 11
                                    num += 1
                                    indice += 1
                                    
                            
                                    
                                        
                                            
                                        
                                except   (ConnectionError, TimeoutError) as errh:
                                    # Se presenta un error se llama la función  reconexión de modo que reinicie la conexión de la computadora si encuentra conectada en 
                                    # wifi
                                    intentos +=1
                                    reconexion()
                                    time.sleep(10)
                                    intentos +=1 
                                    print("Se presentó problemas de conexión")
                                    print(f"\n\n Intento: {intentos}\n\n")
                                                                        
                                except requests.exceptions.HTTPError as errh:
                                    # Esta es la excepción cuando no se obtiene datos de la API
                                    # Se hace un tiempo de espera de un minuto con el fin de dar oportunidad de que cargue y pueda funcionar el servidor
                                    intentos +=1
                                    print(f"Error HTTP al obtener la obra de ID: {obra_id}: {errh}")
                                    reconexion()
                                    time.sleep(10)
                                    intentos +=1 
                                    print(f"\n\n Intento: {intentos}\n\n")
                                
                                except requests.exceptions.JSONDecodeError as e:
                                    print(f"Error de formato JSON para la obra de ID: {obra_id}: {e}")
                                    time.sleep(10)
                                    intentos +=1 
                                    print(f"\n\n Intento: {intentos}\n\n")
                
                        while True: 
                            opcion = int(input(f"""
                                  Indique la opción que desea tomar:
                                  
                                    1.- Seleccionar ID :
                                    2.- Revisar otras obras: 
                                    3.- Cambiar {tipo}
                                    4.- Salir al menú principal
                                    
                                    Indicar opción : """).strip())
                            
                            try:
                                if opcion == 1:
                                    while True:
                                        print("")
                                        for obra in conjunto:
                                            print(obra)
                                        selec_id = int(input(" \n\nSeleccionar el número que acompaña la información de la obra: "))
                                        selec_id -= 1
                                        try:
                                            id = id_obra[selec_id]
                                            salida = True
                                            return id, salida
                                        except ValueError: 
                                            print("\n\nSelecciona el valor de las obras disponibles\n\n")
                                        except IndexError:
                                            print("\n\nIngresaste un número fuera del rango de obras disponibles\n\n")
                                elif opcion == 2: 
                                      break
                                elif opcion == 3:
                                    id =  " No seleccionado "
                                    salida = False
                                    return id, salida
                                elif opcion == 4:
                                    id =  " No seleccionado "
                                    salida = True
                                    return id, salida
                                else: 
                                    print("\n No ingresaste ninguna de las opciones \n")
                            except ValueError:
                                print("\n\nDebe ingresar número en función a lo indicado\n\n")
         
                        
                    else: 
                        print("Ingresó los datos equivocados")
                except ValueError:
                    print("\n\nDebe ingresar número en función a lo indicado\n\n")
         
        
            
tipo = "artistas"
caracteristica = "重武 Shigetake"
response = busqueda_id(tipo,caracteristica)
id,salida = mostrar(response, tipo)
print(id)