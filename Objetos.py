class Departamento:
    def __init__(self, id, nombre, obras):
        pass
    
class Autor:
    def __init__(self, nombre, nacionalidad, obras, fecha_nacimiento, fecha_fallecimiento):
        pass

class Obra(Autor):
    def __init__(self, id, titulo, autor, nacionalidad,  fecha_nacimiento, fecha_fallecimiento, tipo, año_creacion, imagen):
        super().__init__(autor, nacionalidad, fecha_nacimiento, fecha_fallecimiento)
        self.id = id
        self.titulo = titulo
        self.tipo = tipo
        self.año_creacion = año_creacion
        self.imagen = imagen