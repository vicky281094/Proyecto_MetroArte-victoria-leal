#Empezamos a defifnir las clases 
#Se tomaran en cuenta solo 2 clases, una para las obras y otra para los departamentos
#Las obras tendran un ID, titulo, autor, año de nacimiento, año de muerte, tipo de obra y una imagen
class obra:
    def __init__(self, ID, Titulo, autor, nacio, nacimineto, muerte, tipo, año, imagen):
        self.ID = ID
        self.Titulo = Titulo
        self.autor = autor
        self.nacio = nacio
        self.nacimineto = nacimineto
        self.muerte = muerte
        self.tipo = tipo
        self.año = año
        self.imagen = imagen


class Departamento:
    def __init__(self, ID, nombre, descripcion):
        self.ID = ID
        self.nombre = nombre
        self.descripcion = descripcion