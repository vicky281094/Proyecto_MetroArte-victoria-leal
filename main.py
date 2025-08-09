# Se importa las librerías del documento Funciones.py
from Funciones import listas_determinada, seleccion, busqueda_id, mostrar, obtener_obra



# Espacio que se mostrará en la pantalla
def main():
    museo = listas_determinada()
    print(" ")
    id = " "
    
    # Sepresenta tres opciones:
    # La primera permite buscar los Ids que cumplan con las condiciones exigidas. Se puede buscar ya sea por Autor, nacionalidad o obra
    # La segunda opción muestra la obra a partir de un id, ya sea, el seleccionado la primera opción o uno que indque el usuario
    # La tercera opción es cerrar el programa
    while True: 
        print("""
              Bienvenidos a Metro Arte, ¿Qué le gustaría hacer?
              
              1.- Buscar obras
              2.- Obtener información de una obra
              3.- Salir """)
        try:
            opcion = int(input("                     Indique su opción: "))
            salida = False
            
            # Esta es la opción 1, el usuario debe seleccionar el tipo de filtro a usar, ya sea el buscarlo por la nacionalidad, autor o departamento
            # Al tomar la decisión, se gurda la selección y pasa por el proceimiento de:
            # En caso de ser departamento o nacionalidad, seleccionar de las opciones disponibles
            # Buscar Id de las obras que cumpla con las condiciones exigidas
            # Mostrar todas o una parte de las obras conseguidas
            # El usuario tiene la posibilidad de seleccionar una obra y guardar su id o si la lista es grande, mostrar parte de la lista de los ids conseguido
            # o usar otro filtro, o, en su defecto, salir al menú principal
            if opcion == 1:
                
                
                while salida == False: 
                    try:
                        decision = int(input("""
                                         Seleccione el número que acompaña al tipo de búsqueda: 
                                         
                                           1.- Autor
                                           2.- Nacionalidad
                                           3.- Departamentos
                                        
                                         > """))
                        
                        if decision == 1:
                            while salida == False:
                                tipo = "Artista"
                                caracteristica =  seleccion(tipo, museo)
                                response = busqueda_id(tipo,caracteristica)
                                id,salida = mostrar(response, tipo)

                            
                        elif decision == 2:
                            while salida == False:
                                tipo = "Nacionalidad" 
                                caracteristica =  seleccion(tipo, museo)
                                response = busqueda_id(tipo,caracteristica)
                                id,salida = mostrar(response, tipo)
                        elif decision == 3:
                            while salida == False:
                                tipo = "Departamento"
                                caracteristica =  seleccion(tipo, museo)
                                response = busqueda_id(tipo,caracteristica)
                                id,salida = mostrar(response, tipo)
                        else:
                            print("Las opciones disponibles son: 1, 2, 3 ")
                    except ValueError:
                        print("Indique su selección por número que acompaña la selección")
            
            
            
            # Esta es la opción 2, permite usar la función de mostrar información de una obra tomando en cuenta el id disponible, si se usó antes la opción 1 y 
            # se decidió guardar el id de una de las obras oservadas, se puede usar dicho id y mostrar infromación más detallada de la obra, además, si es posible, 
            # se mostrará una imagen
            # En caso de tener id o no querer usar esta opción, el usuario tiene la posibilidad de escribir un id que pertenezca a una de las obras y de ser así
            # se mostrará su información 
            elif opcion == 2: 
                while True:
                    try:
                        decision = int(input("""
                                             Deseas usar:
                                               1.- Mostar obra con el id encontrado en mostrar obras
                                               2.- Indicar id 
                                               > """))
                        print(" ")
                        if decision == 1:
                            if id == " ":
                                print("\n Debes buscar el id primero \n")
                            else:
                                obra = obtener_obra(id)
                                obra.show()
                                break
                            break
                        elif decision == 2:
                            while True:
                                try:
                                    id = int(input("Indique Id: "))
                                    print(" ")
                                    obra = obtener_obra(id)
                                    obra.show()
                                    break
                                except ValueError:
                                    print("\n El Id está compuesto unicamente de números \n")
                                except AttributeError:
                                    print(f" \n No se consiguió ninguna obra con el id {id}, intentelo nuevamente \n")
                            break
                        else:
                            print(" Las opciones se presenta 1 o 2")
                            
                            
                    except ValueError:
                        print("Indique su respuesta en número")
            
            # Esta última opción es simplemente cerrar el programa
            elif opcion == 3: 
                print("\n Hasta la próxima")
                break
        except ValueError: 
            ("Ingrese las opciones disponibles [1, 2, 3]")

main()