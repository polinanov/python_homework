class BaseField:
    name = ''
    field_type = ''

    def __set_name__(self, owner, name_field):
        self.name = name_field

    def get_value(self, name_insert):
        if self.field_type == 'text':
            return f'\'{name_insert.__dict__[self.name]}\''
        return name_insert.__dict__[self.name]


class CharField(BaseField):
    field_type = 'text'

    def __init__(self, max_length):
        if not isinstance(max_length, int):
            raise TypeError(f'Value max_length  must be int')
        self.max_length = max_length
        self.min_length = 0

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError(f'Value {self.name} must be {self.field_type}')

        if self.max_length > len(value) > self.min_length:
            instance.__dict__[self.name] = value
        else:
            raise ValueError(f'Value {self.name} must be > {self.min_length} and < {self.max_length}')


class IntegerField(BaseField):
    field_type = 'int'

    def __init__(self, min_value):
        if not isinstance(min_value, int):
            raise TypeError(f'Value min_value must be int')
        self.min_value = min_value

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise ValueError(f'Value {self.name} must be {self.field_type}')

        if value > self.min_value:
            instance.__dict__[self.name] = value
        else:
            raise ValueError(f'Value {self.name} must be > {self.min_value}')
