from db.db import Database
from models.__init__ import models, Generic, Many

db = Database()
db.sync(models)

db.insert(Generic(**{"id_person":2,"nome":"abias","descricao":"muito legal"}))