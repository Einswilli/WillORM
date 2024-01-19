#coding: utf-8
from validators import ValidationError
from ..connectors import *
import inspect

def generate_table_creation_script(model):
    """ return a creation script for a given model """

    query=f'CREATE TABLE IF NOT EXISTS {model.__name__} ('
    query+=', '.join([f'{k} {v.get_script()}' for k,v in model.attributes.iteritems()])
    query+=')'
    print(query)
    return query

class Model():
    """ Base class for all models """
    
    def __init__(self):
        self.attributes={}

    def __enter__(self):
        self.create_table()

    def set_attributes(self,**attributes):
        for k,v in attributes.items():
            if isinstance(v,BaseField):
                self.attributes[k] = v

    def create_table(self):
        curs,conn=SqliteConnector().get_connection()
        curs.execute(generate_table_creation_script(self.__class__))
        conn.commit()

    def save(self):
        # first get DB connection and cursor
        curs,conn=SqliteConnector().get_connection()

        # getting all attributes of the current model
        members=inspect.getmembers(self,lambda m:not(inspect.isroutine(m)))
        members_name=[a[0] for a in members if not (a[0].startswith('__')) and a[0].endswith('__')]

        # db columns placeholders
        placeholders=', '.join('?'*len(members_name) )
        columns=', '.join(members_name)

        query=f'INSERT INTO {self.__class__.__name__} ({columns}) VALUES ({placeholders})'
        values=[getattr(self,key) for key in members_name]
        curs.execute(query,values)

class BaseField:
    """A base class for all fields of a model"""

    def __init__(self,unique=True,null=False,validators=[]):
        self.unique=unique
        self.null=null
        self.validators=validators

    def get_script(self):
        """Return the string representation of current field creation script"""
        raise NotImplementedError

    def validate(self,value):
        """ return a boolean result of all validators check """
        if self.validators!=[]:
            for v in self.validators:v.check(value)

class AutoField(BaseField):
    """ """

    def __init__(self,primary_key=True,length=11,unique=True,null=False,validators=[],**kwargs):
        self.primary_key=primary_key
        self.length=length
        super().__init__(unique,null,validators)
        
    @property
    def value(self):
        return self.value

    def get_script(self):
        '''Return the string representation of current field creation script'''
        # check validation
        self.validate(self.value)

        s=f'INTEGER ({self.length})'
        if self.primary_key:
            s+=' PRIMARY KEY'
        if self.unique:
            s+=' UNIQUE'
        if not self.null:
            s+=' NOT NULL'
        return s

class StringField(BaseField):

    def __init__(self,default=None,unique=True,null=False,max_length=255,min_length=1,validators=[],**kwargs):
        self.default=default
        self.min_length=min_length
        self.max_length=max_length
        super().__init__(unique,null,validators)

    @property
    def value(self):
        return self.value

    def get_script(self):

        # check validation
        self.validate(self.value)

        s=f'VARCHAR({self.max_length})'
        if self.unique:
            s+=' UNIQUE'
        if not self.null:
            s+=' NOT NULL'
        return s

    def check_length(self):
        if len(self.value)<self.min_length:
            raise 


class ReferenceField(BaseField):

    def __init__(self,model,null=False,mode='CASCADE'):
        self.value=None
        self.null=null
        self.mode=mode
        
        # check if model is valid
        if not isinstance(model,Model):
            raise ValueError(f'FIrst argument must be a instance of "Model" not {type(model)}')
        self.model=model

    def get_script(self):
        # check validation

        self.validate(self.value)