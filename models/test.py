class Test:
    def __init__(self, **entries):
        self.teste = "VARCHAR(255)"
        self.__dict__.update(entries)

    associations = False
