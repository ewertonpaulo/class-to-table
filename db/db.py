import psycopg2, json
from collections import namedtuple
from auth import dbname,host,password,port,user

class Database:
    def __init__(self):
        try:
            self.connect()
        except:
            print("Failure in connection")
    
    def connect(self):
        self.connection = psycopg2.connect(
            "dbname='%s' user='%s' host='%s' password='%s'"
            %(dbname,user,host,password))
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        # self.dict_cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def sync(self, models):
        # sync all models from a list of models
        import random
        while len(models) > 0:
            try:
                m = models[0]
                self.create(m)
                del(models[0])
            except:
                random.shuffle(models)

    def create(self, model):
        # create model by atributes
        name = type(model).__name__
        dic_m = model.__dict__
        create_table_command = ("CREATE TABLE IF NOT EXISTS %s (id serial PRIMARY KEY NOT NULL)" %(name))
        self.cursor.execute(create_table_command)
        self.add_columns(dic_m, name)
        if model.associations: # verify if the model has associations
            ass = model.associations
            for i in ass:
                if i == "has_one":
                    self.has_one(model)
                else:
                    self.has_many(model, ass[i])

    def add_columns(self, columns, name):
        # add colums to an model
        for i in columns:
            command = ("ALTER TABLE %s ADD COLUMN IF NOT EXISTS %s %s" %(name, i, columns[i]))
            self.cursor.execute(command)

    def insert(self, model):
        name = type(model).__name__
        itens, values = self.itens_values_split(model)
        command = "INSERT INTO %s (%s) VALUES%s" %(name, ",".join(itens), values)
        self.cursor.execute(command)

    def itens_values_split(self, model):
        it, vl = [], []
        dic_m = model.__dict__
        for i in dic_m:
            it.append(i)
            vl.append(dic_m[i])
        return (tuple(it),tuple(vl))

    def has_one(self, model1, cascade=True):
        if cascade:
            cascade = "ON DELETE CASCADE"
        one = type(model1.associations['has_one']).__name__
        name = type(model1).__name__
        constraint_name = name+"_"+one
        column = {constraint_name:'INT4'}
        self.add_columns(column, one)
        self.add_columns(column, name)
        command = "ALTER TABLE %s \
                ADD CONSTRAINT %s FOREIGN KEY (%s) REFERENCES %s (id) %s;"  %(name, constraint_name, constraint_name, one, cascade)
        self.cursor.execute(command)

    def has_many(self, model1, model2, cascade=True):
        if cascade:
            cascade = "ON DELETE CASCADE"
        name1 = type(model1).__name__
        name2 = type(model2).__name__
        name_table = name1+"_"+name2
        create_table_command = ("CREATE TABLE IF NOT EXISTS %s (id serial PRIMARY KEY NOT NULL)" %(name_table))
        self.cursor.execute(create_table_command)
        columns = {name1:'INT4', name2:'INT4'}
        self.add_columns(columns, name_table)

    def get_one(self):
        return None
