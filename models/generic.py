from .test import Test
from .many import Many

class Generic:
    def __init__(self, **entries):
        self.id_person= "INT"
        self.nome = "VARCHAR(255)"
        self.descricao = "VARCHAR(255)"
        self.__dict__.update(entries)

    associations = {'has_one':Test(), 'has_many': Many()}
