#coding:utf-8
import re

class ValidationError(ValueError):

    def __init__(self, *args):
        super().__init__(*args)

class BaseValidator:
    """ base class for all validators """

    def check(self):
        """ check the validity of a given BaseField value """
        raise NotImplementedError

class MinLenValidator(BaseValidator):

    def __init__(self,min_len=0):
        self.min_len=min_len

    def check(self,value):
        # value must be a str
        if (str(type(value))==str(type("hello"))):
            if len(value)<self.min_len:
                raise ValueError(f'value length must be lower than {self.min_len}')
        else:
            raise TypeError(f'value must be a "str" not "{str(type(value))}"')

class MaxLenValidator(BaseValidator):

    def __init__(self,max_len=0):
        self.max_len=max_len

    def check(self,value):
        # value must be a str
        if (str(type(value))==str(type("hello"))):
            if len(value)>self.max_len:
                raise ValueError(f'value length must be greater than {self.max_len}')
        else:
            raise TypeError(f'value must be a "str" not "{str(type(value))}"')

class RegexValidator(BaseValidator):

    def __init__(self, pattern):
        self.pattern=pattern

    def check(self,value):
        # value must be a string
        if (str(type(value))==str(type("hello"))):
            # then match pattern on value
            if re.match(self.pattern,value) is None:
                raise ValueError(f'value must match this pattern "{self.pattern}"')
        else:
            raise TypeError(f'value must be a "str" not "{str(type(value))}"')

class RequiredValidator(BaseValidator):

    def __init__(self):
        # value cannot be None
        pass

    def check(self,value):
        if value in (None,''):
            raise ValueError('Value is required')

class MinValidator(BaseValidator):

    def __init__(self,min_value=0):
        self.min_value=min_value

    def check(self,value):
        # first chech if value is int or float
        if not str(type(value)) in (str(type(1)),str(float(1.1))):
            raise TypeError('the value type must be an "int" or "float"')

        # then if value is out of range
        if value<self.min_value:
            raise ValueError(f'Value mus be greater than {self.max_value}')

class MaxValidator(BaseValidator):

    def __init__(self,max_value=0):
        self.max_value=max_value

    def check(self,value):
        # first chech if value is int or float
        if not str(type(value)) in (str(type(1)),str(float(1.1))):
            raise TypeError('the value type must be an "int" or "float"')

        # then if value is out of range
        if value>self.max_value:
            raise ValueError(f'Value mus be lower than {self.max_value}')
        