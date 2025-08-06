#Definición de clases

# Clase que guarda las listas de departamentos, autores y nacionalidades disponibles
class Museo:
    def __init__(self, departamentos, autor, nacionalidades):
        self.departamentos = departamentos
        self.autor = autor        
        self.nacionalidades = nacionalidades

# Clase para los objetos departamentos
class Departamento:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

# Clase para los objetos Autor
class Autor:
    def __init__(self, nombre, nacionalidad, fecha_nacimiento, fecha_fallecimiento):
        self.nombre = nombre
        self.nacionalidad = nacionalidad 
        self.fecha_nacimiento = fecha_nacimiento
        self.fecha_fallecimiento = fecha_fallecimiento
        

# Clase para los objetos Obra
class Obra(Autor):
    def __init__(self, id, titulo, autor, nacionalidad,  fecha_nacimiento, fecha_fallecimiento, tipo, año_creacion, imagen):
        super().__init__(autor, nacionalidad, fecha_nacimiento, fecha_fallecimiento)
        self.id = id
        self.titulo = titulo
        self.tipo = tipo
        self.año_creacion = año_creacion
        self.imagen = imagen