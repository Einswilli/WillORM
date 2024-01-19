import sys
sys.path.append('../')
from ...WILORM.databases.models import AutoField, Model, StringField

class User(Model):

    id=AutoField(primary_key=True,unique=True)
    name=StringField(unique=False)
    