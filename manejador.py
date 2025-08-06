# Se importa la librerías, ya se para manejar data de una API, manejar el tiempo en la que realiza acciones el dispositvo, manejo de archivos csv
# y manejo de funciones de sistema
import requests 
import time
import csv
import subprocess

#Función de uso opcional, su objetivo es revisar por cada obra todos los departamentos, artistas y nacionalidades disponibles
def revision():
    
    # Usar la API de las ID de objetos y generar una lista de todos los ID
    url = 'https://collectionapi.metmuseum.org/public/collection/v1/objects'
    obras = requests.get(url)
    obras = obras.json()
    
    # Usar la API para obtener los Departamentos que sus ID son reconocidos y generar un diccionario.
    # El diccionario contiene dos llaves
    dep_url = 'https://collectionapi.metmuseum.org/public/collection/v1/departments'
    departamentos = requests.get(dep_url)
    departamentos = departamentos.json()
    departamentos = departamentos['departments']
    
    # El Json obtenido del link para los departamentos tiene dos llaves, la primera, 'totals' contiene el número que indica el total de departamentos 
    # disponibles y la otra llave, 'departments' contiene una lista de diccionarios, donde cada diccionario contiene 
    # el id (departmentId) y el nombre (displayName) del departamento
    
    
    
    # Se crea otro variable con el objetivo de estudiar la media de obras que hay por cada departamentos disponibles
    dicc_departamentos = departamentos
    
    # Establecer lista de nacionalidades, aquí se resguarda cada nacionalidad que se consiga en el objeto
    nacionalidades = []
    
    # Establecer una lista de diccionarios sobre la artista. Por cada artista se contiene Nombre del artista 
    # nacionalidad del artista, fecha de nacimiento y fecha de muerte
    artistas = []
    
    
    # Se crea otro lista de diccionarios con el objetivo de estudiar la media de obras que hay por cada departamento, agregando el ID del objeto
    # relacionado a este y la cantidad de ID que contiene
    
    # Por la posibilidad de conseguir otros departamentos, indicaremos el último ID 
    ult_id = 0
    for departamento in dicc_departamentos:
        departamento['objectID'] = []
        departamento['cantidad'] = 0
        ult_id = departamento['departmentId']
    
    # Con el fin de observar la cantidad de obras que hay por la nacionalidad del artistas y por cada artista, se crean un diccionario para las
    # nacionalidades y una lista de diccionarios para los artistas 
    dicc_nacionalidades = {}
    dicc_artistas = []
    
    # Se usa este diccionario con el objetivo de hacer pruebas para extraer la información contenida por cada obra
    dicc_obras = {}
    
    # Se usa para contar la cantidad de objetos observados
    numero = 0
    
    #Se irá  por ID de la ista obras
    for obra in obras['objectIDs']:
        # A fin de que  funcione todo correctamente, se dará 3 intentos para corregir las excepciones, en caso de no poderse se culminará el 
        # proceso hasta lo obtenido
        max_intentos = 3
        intentos = 0
        while intentos < max_intentos:
            try:
                
                #Se busca en la API la información de la obra, usando el ID, convirtiendo en string el ID y en caso de obtener la información
                #se suma en numero la cantidad de obras revisadas 
                obra = str(obra)
                url = f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{obra}'
                obra_detalle = requests.get(url)
                obra_detalle = obra_detalle.json()
                numero += 1
                
                # Se realiza verficación de la data disponible en el campo que contiene el ID
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
                # Se aprovecha de ser agregado a la lista de nacionalidades que se guardara en el csv, se revisa si en la lista
                # nacionalidades se encuentra repetido la nacionalidad y se ordena la lista en orden alfabético de la a hasta la z
                if 'artistNationality' in obra_detalle:
                    if not obra_detalle['artistNationality']:
                        nacionalidad = 'Desconocido'
                        nacionalidades.append(nacionalidad)
                        if len(nacionalidades) > 2:
                            nacionalidades = set(nacionalidades)
                            nacionalidades = list(nacionalidades)
                            nacionalidades.sort()    
                            
                    else:
                        nacionalidad = obra_detalle['artistNationality']
                        nacionalidades.append(nacionalidad)
                        if len(nacionalidades) > 2:
                            nacionalidades = set(nacionalidades)
                            nacionalidades = list(nacionalidades)
                            nacionalidades.sort()
                
                            
                            
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
                
                # Se realiza verficación de la data disponible en el campo si contiene el  link principal de la imagen
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

                
                # Este espacio es para el manejo de la data sobre la nacionalidades que se usara para estudiar la media de obras que hay 
                # por nacionalidad
                if 'artistNationality' in obra_detalle:

                    # Usamos el nombre de la nacionalidad como clave del diccionario
                    if nacionalidad not in dicc_nacionalidades:
                        # Si la nacionalidad no existe, la creamos
                        dicc_nacionalidades[nacionalidad] = {
                            'origen': nacionalidad,
                            'objectID': [obra_id],
                            'cantidad': 1
                        }
                    else:
                        # Si ya existe, simplemente actualizamos sus valores
                        dicc_nacionalidades[nacionalidad]['objectID'].append(obra_id)
                        dicc_nacionalidades[nacionalidad]['cantidad'] += 1
                
                
                
                # Se realiza verficación de la data disponible en el campo si contiene el nombre del artista, a su vez se define la como se vería
                # la información de dicho artista tomando como diccionario y guardalo en la lista de artista que usará para guardar en el csv.
                
                #  Se elimina datos repetidos y se ordena de a hasta la z
                if 'artistDisplayName' in obra_detalle:
                    if not obra_detalle['artistDisplayName']:
                        nombre = 'Desconocido'
                        artista = {'artista':nombre,'nacionalidad':nacionalidad,'nacimiento': nacimiento, 'muerte': muerte}
                        artistas.append(artista)
                        if len(artistas) > 2:
                            artistas_sin_duplicados = [dict(t) for t in {tuple(d.items()) for d in artistas}]
                            artistas = sorted(artistas_sin_duplicados, key=lambda artistas: artistas['artista'], reverse=False)
                            
                        
                    else:
                        nombre = obra_detalle['artistDisplayName']
                        artista = {'artista':nombre,'nacionalidad':nacionalidad,'nacimiento': nacimiento, 'muerte': muerte}
                        artistas.append(artista)
                        if len(artistas) > 2:
                            artistas_sin_duplicados = [dict(t) for t in {tuple(d.items()) for d in artistas}]
                            artistas = sorted(artistas_sin_duplicados, key=lambda artistas: artistas['artista'], reverse=False)
                
                # Se realiza verficación de la data disponible en el campo si contiene el nombre del artista. Realiza el proceso anterior pero enfocado a la lista
                # de artistas que se enfoca para estudiar la media de obras por cada artista 
                if 'artistDisplayName' in obra_detalle:
                    verificar = 0
                    for art in dicc_artistas:
                        if art['artista'] == nombre:
                            verificar = 1
                            
                            art['objectID'].append(obra_id)
                            art['cantidad'] += 1
                            
                    if verificar ==  0:
                        artista = {'artista':nombre,'nacionalidad':nacionalidad,'nacimiento': nacimiento, 'muerte': muerte, 'objectID': [obra_id], 'cantidad': 1}
                        dicc_artistas.append(artista)
                        if len(artistas) > 2:
                            artistas_sin_duplicados = [dict(t) for t in {tuple(d.items()) for d in artistas}]
                            artistas = sorted(artistas_sin_duplicados, key=lambda artistas: artistas['artista'], reverse=False)
        
                        
                
                # Se realiza verficación de la data disponible en el campo si contiene departamento relacionado a la obra y se agrega a la lista
                # de departamentos que se usa para estudiar la media de obras que hay por cada departamentos
                if 'department' in obra_detalle: 
                    verificar = 0   
                    for dep in dicc_departamentos:
                        if dep['displayName'] == departamento:
                            verificar = 1
                            if 'objectID' in dep:
                                dep['objectID'].append(obra_id)
                                dep['cantidad'] += 1
                            else:
                                dep['objectID'] = [obra_id]
                                dep['cantidad'] += 1
                    if verificar ==  0:
                        ult_id +=1
                        nuevo = {'departmentId':ult_id, 'displayName':departamento, 'objectID': [obra_id], 'cantidad':1}
                        dicc_departamentos.append(nuevo)
                                
                # Con el fin de observar la presentación de datos que se presentaría en un objeto de obra, se usará los datos obtenidos anteriormeente
                # y se imprimirá para comprobar lo que contiene cada dato
                if 'objectID' in obra_detalle:
                
                    dicc_obras[obra_id] = {'objectID':obra_id, 
                                        'title': titulo, 
                                        'artist': artista, 
                                        'nacionalidad': nacionalidad, 
                                        'nacimiento': nacimiento,
                                        'muerte': muerte,
                                        'classification': clasificacion,
                                        'fecha': fecha,
                                        'imagen': imagen,
                                        'department': departamento}
                
                    print(f"""{numero}.- {titulo}:
                          Clasificación: {clasificacion}
                          Departamento: {departamento}
                          Fecha: {fecha} 
                          Sobre el artista: 
                            - Nombre: {artista['artista']} 
                            - Nacionalidad: {nacionalidad}
                            - Nacimiento: {nacimiento}
                            - Muerte: {muerte} 
                          Imagen: {imagen}\n""")
                
                # Se guarda los datos de artistas en un csv dentro de la carpeta listas.
                # Esto se guardará con los datos que se muestran en la cabecera, ya que le objetivo de proyecto es a partir del nombree del artista, obtener información
                # de la obra
                cabeceras = ['artista','nacionalidad','nacimiento', 'muerte']
                with open(file = 'listas/artistas.csv', mode='w', encoding='utf-8',newline=''  ) as f :
                    f = csv.DictWriter(f, fieldnames=cabeceras)
                    f.writeheader()
                    f.writerows(artistas) 
                
                
                # Se guarda los datos de nacionalidades en un csv dentro de la carpeta listas, solo contendrá el nombre de las nacionalidades conseguidos
                with open(file = 'listas/nacionalidades.csv', mode='w', encoding='utf-8', newline='' ) as f :
                    writer = csv.writer(f)
                    for nacionalidad in nacionalidades:
                        writer.writerow([nacionalidad])
                
                #  Se guarda los datos de departamento en un csv dentro de la carpeta listas, por cada fila se contiene el id y el nombre de cada departamento obetenido
                with open(file="listas/departamentos.csv", mode='w', encoding='utf-8', newline='')  as f: 
                    writer = csv.writer(f)
                    writer.writerow(['departmentId', 'displayName'])
                    for departamento in departamentos:
                        writer.writerow([departamento['departmentId'], departamento['displayName']])
                
                # Al no presentar errores se continua con la siguiente ID de la lista de ID 's 
                intentos = 4
                
                
            except   (ConnectionError, TimeoutError) as errh:
                # Se presenta un error se llama la función  reconexión de modo que reinicie la conexión de la computadora si encuentra conectada en 
                # wifi
                intentos +=1
                reconexion()
                                                    
            except requests.exceptions.HTTPError as errh:
                # Esta es la excepción cuando no se obtiene datos de la API
                # Se hace un tiempo de espera de un minuto con el fin de dar oportunidad de que cargue y pueda funcionar el servidor
                intentos +=1
                print(f"Error HTTP al obtener la obra {obra_id}: {errh}")
                time.sleep(60)
        
        
       # Como se ha presentado errores al realizar consultas lo más rápido posible, se establece un tiempo de espera de 3 segundos con el
       # fin de evitar generar errores
        time.sleep(3)
    
    
    # En caso de poder conseguido analizar todo los IDs puede indicar el estudio esperado
    
    # Se saca la media tanto de las obras los cuales contiene la nacionalidad del artista y media de los obras tomando en cuenta aquellas que no 
    # presenta nacionalidad del artista y se muestra los resultados
    n = 0
    m = 0 
    l = 0
    o = 0
    
    lista_nacionalidades = dicc_nacionalidades.values()
    for  nacionalidad in lista_nacionalidades: 
        if nacionalidad['origen'] == 'Desconocido':
            l += 0
            o += 0
        else:
            l += nacionalidad['cantidad'] 
            o += 1
        n += 1
        m += nacionalidad['cantidad'] 
    media = m/n
    
    media_nD = l/o
    
    print(f"""   Por cada nacionalidad hay una media de {media} obras, sin tomar en cuenta las obras 
que se desconoce la nacionalidad se tuviera {media_nD} obras por cada nacionalidad. Total de nacionalidades {n} \n\n""")
    
    
    # Se saca la media tanto de las obras los cuales contiene  artistas y media de los obras tomando en cuenta aquellas que no 
    # presenta información de los artistas y se muestra los resultados
    l = 0
    n = 0
    m = 0
    o = 0
    for artista in dicc_artistas:
        if  artista['artista'] == 'Desconocido':
            l += 0
            o += 0
        else:
            l += artista['cantidad']    
            if o == 0:
                o = 1
        n += 1
        m += artista['cantidad'] 
    media = m/n
    media_nD = l/o
    print(f"""   Por cada artista hay una media de {media} obras, sin tomar en cuenta las obras 
que se desconoce el artista se tuviera {media_nD} obras por cada artista. Total de artista {n} \n\n""")
   
   
    # Se saca la media tanto de las obras los cuales contiene información del departamento al que pertenece y media de los obras tomando en cuenta aquellas que no 
    # presenta infromación del departament y se muestra los resultados    
    l = 0
    n = 0
    m = 0
    o = 0
    for departamento in dicc_departamentos:
        if  departamento['displayName'] == 'Desconocido':
            l += 0
            o += 0
        else:
            l += departamento['cantidad'] 
            o += 1
        m += departamento['cantidad']
        n += 1
    media = m/n
    media_nD = l/o
    print(f"""   Por cada departamento hay una media de {media} obras, sin tomar en cuenta las obras 
que se desconoce el departamento se tuviera {media_nD} obras por cada departamento. Total de departamentos {n} \n\n""")
        
    
    
    
     
# Esta función está enfocado en desconectar y reconectar el dispositivo en caso de haber posibles problemas de conexión
# Solo funciona, si solo si, el visual code está abierto como administrador
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
        time.sleep(60)

    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")
        print("Asegúrate de que el script se ejecuta como Administrador.")
    except FileNotFoundError:
        print("El comando 'netsh' no se encontró. Verifica tu instalación de Windows.")
  
        
            
        
revision()
    


