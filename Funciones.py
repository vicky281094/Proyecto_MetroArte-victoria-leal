
# Se importa librería para manejar los datos disponibles
import requests
import time
from PIL import Image
from Objetos import Departamento, Museo, Obra
import io

# Se define la lista
departamentos = [] 
nacionalidades = [] 
    
            

# Esta función nos ofrece los datos que se ofrece en la API respecto a departamentos y el csv que se tiene en Google Drive, retornando el objeto museo
# que contiene las listas de departamentos y nacionalidades
def listas_determinada():
    # Se establece las listas a usar. Por la asignatura se ofrece una lista de de nacionalidades, mientras la API ofrece una lista de departamentos,
    # cada departamento está compuesto por el id y el nombre del departamento
    nacionalidades = []
    departamentos = []
    
    # Este es el url donde se encuentra las nacionalidades, está ajustado para descargar
    url_nacionalidades = "https://drive.google.com/uc?export=download&id=1tJEU6_VEeO6xFH8fssSfkw4M8MaN6U5A"
    
    try:
        # Se pbusca obtener datos que se dará en forma de texto, una abajo de otra
        response = requests.get(url_nacionalidades)
        response.raise_for_status() # Lanza un error si hay un problema de conexión

        # Leemos el contenido como texto en lugar de JSON
        texto_nacionalidades = response.text
        
        # Procesamos cada línea del texto para crear una lista de nacionalidades
        nacionalidades = texto_nacionalidades.strip().split('\n')
        
        # Eliminamos espacios en blanco extra de cada nacionalidad y se guarda todas las nacionalidades en una lista
        nacionalidades = [n.strip() for n in nacionalidades if n.strip()]
        nacionalidades = nacionalidades[1:]
        
        print("Datos de nacionalidades cargados exitosamente.")
        
        
        # Es una excepción en caso de que no se logre bajar la data del url
    except requests.exceptions.RequestException as e:
        print(f"\n\n Error al descargar o procesar el archivo: {e} \n\n")
        

    # Este es link que ofrece la API, donde se resguarda una lista de departamentos disponibles
    url_departamentos = "https://collectionapi.metmuseum.org/public/collection/v1/departments"
    
    try:
        #Se baja la data de la API y se verifica si se logró bajar
        response = requests.get(url_departamentos)
        response.raise_for_status()
        
        # Lo obtenido se convierte en formato Json para mejor manejo de la data
        departamentos = response.json()
       
       # La API al pedir la data se obtiene un diccionario de dos keys, por lo que interés es el key 'departments' que contiene la lista
        departamentos_lista = departamentos['departments']
        departamentos = []
        
        # Dentro de la lista, se presenta un diccionario por cada departamento que contiene el id y el nombre del respectivo departamento
        # Se decide  definir el objeto Departamento y agregarlo en una lista
        for dep in departamentos_lista:
            departamento = Departamento(dep['departmentId'],dep['displayName'])
            departamentos.append(departamento)
        
        print("Datos de departamentos cargados exitosamente.")
        
    # Se presenta los posibles errores
    except requests.exceptions.RequestException as e:
        print(f"\n\n Error al descargar o procesar el archivo: {e} \n\n")
    
    # Las listas conseguidas se guardan en el objeto museo
    museo = Museo(departamentos,nacionalidades)
    
    print(" ")
    return museo 
        


# Función que buscas los id, para ello, según el filtro que se seleccione (Nacionalidad, Artista, Departamento), se seleccionará un url que facilite la búsqueda, 
# retornando en una lista de los ids, en realidad, un diccionario
# que cumpla con los requisitos
def busqueda_id(tipo, caracteristica):
    
    
    if tipo == "Nacionalidad":
        url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?q={caracteristica}"
        
    
    #Al ser Departamento el tipo de búsqueda, la característica seleccionada es una objeto del tipo departamento, el cual está compuesto id y nombre    
    elif tipo == "Departamento":
        id = caracteristica.id
        q = caracteristica.nombre
        url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?departmentId={id}&q={q}"
        
        
    else:
        url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?artistOrCulture=true&q={caracteristica}"
        
        
    
    response = requests.get(url)        
    response = response.json()
    
    
    return response


# Función encargada de mostrar las obras de la listas ids conseguidas anteriormente. Se mostrará el ID, nombre de la obra y el autor de la obra.
# En caso de haber más de 30 obras, el usuario podrá indicar la cantidadde obras que desea mostrar e indicar de las obras disponibles cuál va ser la primera en 
# ser mostrada            
# Permite seleccionar una obra de las conseguidas y obtener su id, la cual será puede ser usada para mostrar a detalle la información de la obra en la otra opción
# que muestra el pograma
def mostrar(response,tipo):
    
    # La lista ids que se menciona, en realidad es un diccionario compuesto por dos key
    # El primero indica el número total de obras conseguidas ('total')
    # Mientras la otra se refiera a la lista de los ids que cumplieron con los requisitos exigidos anteriormente
    total = response['total']
    Ids = response['objectIDs']
    
    
    # Se presenta los casos en función a la cantidad de ID conseguidos:
    # Si no se consigue ninguna obra, se retornará sin ninguna obra y con salida verdadero, de modo que el usuario tenga la poibilidad de usar otro método de búsqueda
    # Si hay más de 30 obras, tiene la posibilidad de seleccionar una obra y usar su id para después, puede observar una parte de la lista, cambiar a otro filtro o volver
    # al menú
    while True:
        if total <= 0: 
            print("No se consiguió ningún elemento") 
            id =  " No seleccionado "
            salida = False
            return id, salida
            
            
        elif total <= 30:
            num = 1
            conjunto =  []
            for obra in Ids:
                max_intentos = 10
                intentos = 0
                while intentos < max_intentos:
                    

                    # A fin de que  funcione todo correctamente, se dará 3 intentos para corregir las excepciones, en caso de no poderse se culminará el 
                    # proceso hasta lo obtenido
                    
                    
                    try:
                        
                        obra = str(obra)
                        url = f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{obra}'
                        obra_detalle = requests.get(url)
                        obra_detalle = obra_detalle.json()
                        
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
                        time.sleep(60)
                        intentos +=1 
                        print("Se presentó problemas de conexión")
                        print(f"\n\n Intento: {intentos}\n\n")
                                                            
                    except requests.exceptions.HTTPError as errh:
                        # Esta es la excepción cuando no se obtiene datos de la API
                        # Se hace un tiempo de espera de un minuto con el fin de dar oportunidad de que cargue y pueda funcionar el servidor
                        intentos +=1
                        print(f"Error HTTP al obtener la obra número {num}: {errh}")
                        time.sleep(30)
                        intentos +=1 
                        print(f"\n\n Intento: {intentos}\n\n")
                    
                    except requests.exceptions.JSONDecodeError as e:
                        print(f"Error de formato JSON para la obra número {num}: {e}")
                        time.sleep(10)
                        intentos +=1 
                        print(f"\n\n Intento: {intentos}\n\n")
                        
            while True: 
                
                
                try:
                    opcion = int(input(f"""
                        Indique la opción que desea tomar:
                        
                        1.- Seleccionar ID :
                        2.- Cambiar {tipo} :
                        3.- Salir al menú principal :
                        
                        Indicar opción : """).strip())
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
                                print(f"""
                                                  
                                                  El ID siguiente obra ha sido seleccionada
                                                  {conjunto[selec_id]} 
                                                  
                                                  """)
                                return id, salida
                            except ValueError: 
                                print("\n\nSelecciona el valor de las obras disponibles\n\n")
                            except IndexError:
                                print("\n\nIngresaste un número fuera del rango de obras disponibles\n\n")
                    elif opcion == 2:
                        id =  " No seleccionado "
                        salida = False
                        print("")
                        return id, salida
                    elif opcion == 3:
                        id =  " No seleccionado "
                        salida = True
                        print("")
                        return id, salida
                    else: 
                        print("\n No ingresaste ninguna de las opciones \n")
                except ValueError:
                    print("\n\nDebe ingresar número en función a lo indicado\n\n")
            
                 
        else: 
            while True:
                
                
                try:
                    print(f""" 
                      Se presenta {total} de obras, por lo que presentará un número limitado de obras, para ello se requiere:
                         - Indicar la cantidad de obras que quieres mostrar, el máximo son 50 obras para presentarse, el mínimo es 1
                         - Indicar a partir de que valor se desea buscar, su posción debes indicarlo desde el 1 hasta {total}
                      """)
                    rango = int(input("Indicar la cantidad de valores: ").strip())
                    pri_obra = int(input("Indicar la poscición del primer valor: ").strip())
                    print(" ")
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
                                    time.sleep(30)
                                    intentos +=1 
                                    print("Se presentó problemas de conexión")
                                    print(f"\n\n Intento: {intentos}\n\n")
                                                                        
                                except requests.exceptions.HTTPError as errh:
                                    # Esta es la excepción cuando no se obtiene datos de la API
                                    # Se hace un tiempo de espera de un minuto con el fin de dar oportunidad de que cargue y pueda funcionar el servidor
                                    intentos +=1
                                    print(f"Error HTTP al obtener la obra número {num}: {errh}")
                                    time.sleep(30)
                                    intentos +=1 
                                    print(f"\n\n Intento: {intentos}\n\n")
                                
                                except requests.exceptions.JSONDecodeError as e:
                                    print(f"Error de formato JSON para la obra número {num}: {e}")
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
                                            print(f"""
                                                  
                                                  El ID siguiente obra ha sido seleccionada
                                                  {conjunto[selec_id]} 
                                                  
                                                  """)
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
                    print("\n\n Debe ingresar número en función a lo indicado \n\n")
         
#Función enfocada en poder seleccionar entre las opciones disponibles:
# Si se seleccionó buscar por artista, al no presentar lista de nombres, se usará lo escrito por el usuario para la búsqueda
# Si se seleccionó buscar por departamento, el usuario se le presentará los departamentos disponibles y tendrá que seleccionar uno de ellos
# Si se seleccionó buscar por nacionalidad, al haber varioas nacionalidades, el usuario deberá escribir ya sea la nacionalidad en inglés o una parte, de modo que se 
# busque las opciones que cumple con lo indicó el usuario 
def seleccion(tipo, museo):
    if tipo == "Nacionalidad":   
        nacionalidades = museo.nacionalidades
        
        while True:
            print(f"""
                  Hay {len(nacionalidades)} nacionalidades disponibles, al ser demasiadas, 
                  vas escribir el nombre de la nacionalidad o en su defecto escribir una parte de la nacionalidad
                  
                  Recordar que las nacionalidades están en inglés
                  
                  """)
            nacion = input("Indicar la nacionalidad: ")
            encontrados = []
            indice = 0
            for nacionalidad in nacionalidades:
                
                if nacion.lower() in nacionalidad.lower():
                    indice += 1
                    print(f"{indice}.- {nacionalidad}")
                    encontrados.append(nacionalidad)
            if len(encontrados) == 0:
                print("\n No se encontraron nacionalidades con dichas caracteristicas \n")
            elif len(encontrados) == 1:
                while True: 
                    opcion = int(input(f"""
                            Indique la opción que desea tomar:
                            
                            1.- Buscar nuevamente la nacionalidad :
                            2.- Seleccionar nacionalidad: 
                            
                            Indicar opción : """).strip())
                    print("")
                    try:
                        if opcion == 1:
                            break
                        elif opcion == 2:
                            caracteristica = encontrados[0]
                            print(f"\n Se ha seleccionado a {caracteristica} como nacionalidad a buscar")
                            return caracteristica 
                
                    except ValueError:
                        print("\n\n No escribió número, trate colocar el número de acuerdo a las opciones disponibles \n\n")
            else: 
                while True: 
                    opcion = int(input(f"""
                            Indique la opción que desea tomar:
                            
                            1.- Buscar nuevamente la nacionalidad :
                            2.- Seleccionar nacionalidad: 
                            
                            Indicar opción : """).strip())
                    print("")
                    try:
                        if opcion == 1:
                            break
                        elif opcion == 2:
                            while True:
                                print("")
                                n = 0
                                for seleccion in encontrados:
                                    n += 1
                                    print(f"{n}.- {seleccion}")
                                selec_nacion = int(input(" \n\nSeleccionar el número que acompaña la información de la obra: "))
                                selec_nacion -= 1
                                try:
                                    caracteristica = encontrados[selec_nacion]
                                    
                                    print(f"""
                                            
                                            La siguiente nacionalidad ha sido seleccionada:
                                            {caracteristica} 
                                            
                                            """)
                                    return caracteristica
                                except ValueError: 
                                    print("\n\nSelecciona el valor de las obras disponibles\n\n")
                                except IndexError:
                                    print("\n\nIngresaste un número fuera del rango de obras disponibles\n\n")
                
                    except ValueError:
                        print("\n\n No escribió número, trate colocar el número de acuerdo a las opciones disponibles \n\n")
                
    elif tipo == "Departamento":
        departamentos = museo.departamentos
        
        while True:
            for departamento in departamentos:
                print(departamento.show())
            try: 
                id = int(input("Seleccione colocando el id del departamento que quiera seleccionar: ").strip())
                print("")
                for departamento in departamentos:
                    opcion_id = int(departamento.id)
                    if id  == opcion_id:
                        caracteristica = departamento
                        print(f"\n Se ha seleccionado el siguiente departamento: {departamento.show()} \n")
                        return caracteristica
                print("\n Seleccione el valor del ID que desea seleccionar \n")
            except ValueError:
                print("\n Ingresó datos erróneos \n")
                                         
    else:
        caracteristica = input("Indique el nombre que desea buscar: ")
        return caracteristica
    
    
# Función de obtener toda la data exigida de la obra, tomando en cuenta el id disponible, se obtendrá: id, nombre de la obra, tipo, fecha de la obra, url de laimagen,
# departamento, además, de la información del autor de la obra, como lo puede ser: nombre del autor, nacionalidad, año de nacimiento y año de muerte.

# Después se creará el objeto obra.
def obtener_obra(id):
    
    while True: 
        try:
            id = str(id)
            url = f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{id}'
            obra_detalle = requests.get(url)
            obra_detalle = obra_detalle.json()
            
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
                    
            # Se realiza verficación de la data disponible en el campo que contiene la nacionalidad del artista.
            if 'artistNationality' in obra_detalle:
                if not obra_detalle['artistNationality']:
                    nacionalidad = 'Desconocido'
                else:
                    nacionalidad = obra_detalle['artistNationality']
                        
            # Se realiza verficación de la data disponible en el campo si contiene la fecha de nacimiento del artista
            if 'artistBeginDate' in obra_detalle:
                if not obra_detalle['artistBeginDate']:
                    nacimiento = 'Desconocido'
                else:
                    nacimiento = obra_detalle['artistBeginDate']
            
            # Se realiza verficación de la data disponible en el campo si contiene la fecha de muerte del artista        
            if 'artistEndDate' in obra_detalle:
                if not obra_detalle['artistEndDate']:
                    muerte = 'Desconocido'
                else:
                    muerte = obra_detalle['artistEndDate']
                    
            # Se realiza verficación de la data disponible en el campo si contiene la clasficación de la obra
            if 'classification' in obra_detalle:
                if not obra_detalle['classification']:
                    clasificacion = 'Desconocido'
                else:
                    clasificacion = obra_detalle['classification']
            
            # Se realiza verficación de la data disponible en el campo si contiene la fecha de la obra
            if 'objectDate' in obra_detalle:
                if not obra_detalle['objectDate']:
                    fecha = 'Desconocido'
                else:
                    fecha = obra_detalle['objectDate']
            
            # Se realiza verficación de la data disponible en el campo si contiene el link de la imagen principal
            if 'primaryImage' in obra_detalle:
                if not obra_detalle['primaryImage']:
                    imagen = 'Desconocido'
                else:
                    imagen = obra_detalle['primaryImage']
                    
            # Se realiza verficación de la data disponible en el campo si contiene el departamento relacionado a la obra
            if 'department' in obra_detalle:
                if not obra_detalle['department']:
                    departamento = 'Desconocido'
                else:
                    departamento = obra_detalle['department']
                                                 
            # Se realiza verficación de la data disponible en el campo si contiene el nombre del artista
            if 'artistDisplayName' in obra_detalle:
                if not obra_detalle['artistDisplayName']:
                    nombre = 'Desconocido'
                    
                else:
                    nombre = obra_detalle['artistDisplayName']
                    
            obra = Obra(obra_id, titulo, nombre, nacionalidad, nacimiento, muerte, clasificacion, fecha, imagen)
            
            return obra
            
            
        except   (ConnectionError, TimeoutError) as e:
                # Se presenta un error se llama la función  reconexión de modo que reinicie la conexión de la computadora si encuentra conectada en 
                # wifi
                print(f"Error en la conexión para obtener la obra de id {id}: {e}")
                time.sleep(10)
                intentos +=1 
                print(f"\n\n Intento: {intentos}\n\n")
                                                    
        except requests.exceptions.HTTPError as e:
            # Esta es la excepción cuando no se obtiene datos de la API
            # Se hace un tiempo de espera de un minuto con el fin de dar oportunidad de que cargue y pueda funcionar el servidor
            
            print(f"Error HTTP al obtener la obra de id {id}: {e}")
            time.sleep(10)
            intentos +=1 
            print(f"\n\n Intento: {intentos}\n\n")
        
        except requests.exceptions.JSONDecodeError as e:
            print(f"Error de formato JSON para la obra de id {id}: {e}")
            time.sleep(10)
            intentos +=1 
            print(f"\n\n Intento: {intentos}\n\n")
        
        except UnboundLocalError as e:
            break


# Función encargada de obetner información de la imagen, descargarla y presentarla
def mostrar_imagen(imagen):
    try:
        imagen = requests.get(imagen, stream=True)
        imagen.raise_for_status()
        
        ver_imagen = io.BytesIO(imagen.content)
        ver_imagen = Image.open(ver_imagen)
        ver_imagen.show()
        
        
        
    except requests.exceptions.RequestException as e:
        print("\n Se presentó problemas con la solicitud \n")
        time.sleep(10)
    
    except IOError as e:
        print(f"Error al procesar la imagen: {e}")
        time.sleep(10)

