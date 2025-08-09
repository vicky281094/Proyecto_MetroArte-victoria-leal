

#Definición de clases

# Clase que guarda las listas de departamentos y nacionalidades disponibles
class Museo:
    def __init__(self, departamentos, nacionalidades):
        self.departamentos = departamentos
        self.nacionalidades = nacionalidades
    def show():
        print(" ")

# Clase para los objetos departamentos
class Departamento:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
    
    def show(self):
        return f"Id: {self.id} - nombre:{self.nombre}"

# Clase para los objetos Obra
class Obra():
    def __init__(self, id, titulo, autor, nacionalidad,  fecha_nacimiento, fecha_fallecimiento, tipo, año_creacion, imagen):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.nacionalidad = nacionalidad
        self.fecha_nacimiento = fecha_nacimiento
        self.fecha_fallecimiento = fecha_fallecimiento
        self.tipo = tipo
        self.año_creacion = año_creacion
        self.imagen = imagen
    
    
    # Función encargada de mostrar el contido de la obra y en casa que el apartado de la imagen sea diferente de  'Desconocido', activará la función mostrar_imagen
    # del archivo Funciones.py para mostrar la imagen
    def show(self):
        print(f"""
              Obra: {self.titulo}
                 - Id: {self.id}
                 - Tipo: {self.tipo}
                 - Autor: 
                    * Nombre: {self.autor}
                    * Nacionalidad: {self.nacionalidad}
                    * Fecha de nacimiento: {self.fecha_nacimiento}
                    * Fecha de fallecimiento: {self.fecha_fallecimiento}""")
        if self.imagen == 'Desconocido':
            print("\n No hay  imagen disponible \n")
        else:
            from Funciones import mostrar_imagen
            mostrar_imagen(self.imagen)
         
            