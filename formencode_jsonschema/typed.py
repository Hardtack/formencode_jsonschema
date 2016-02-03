from formencode.api import FancyValidator, NoDefault


class JSONTyped(FancyValidator):
    """
    Wrap formencode validator with JSON schema's types & properties. ::

        validator = JSONTyped(
            {'type': 'string'},
            validators.UnicodeString(),
            required=True,
            description="Some important field",
        )

    """
    __unpackargs__ = ('json_type', 'validator')

    required = NoDefault
    description = None

    def _convert_to_python(self, value, state=None):
        return self.validator.to_python(value, state)

    def _convert_from_python(self, value, state=None):
        return self.validator.from_python(value, state)


class ObjectTyped(JSONTyped):
    """Wrap formencode validator with object type of JSON Schema"""
    def __init__(self, validator, *args, **kwargs):
        super().__init__({
            'type': 'object',
        }, validator, *args, **kwargs)


class ArrrayTyped(JSONTyped):
    """Wrap formencode validator with array type of JSON Schema"""
    def __init__(self, validator, *args, **kwargs):
        super().__init__({
            'type': 'array',
        }, validator, *args, **kwargs)


class DateTyped(JSONTyped):
    """Wrap formencode validator with date type of JSON Schema"""
    def __init__(self, validator, *args, **kwargs):
        super().__init__({
            'type': 'string',
            'format': 'date',
        }, validator, *args, **kwargs)


class TimeTyped(JSONTyped):
    """Wrap formencode validator with time type of JSON Schema"""
    def __init__(self, validator, *args, **kwargs):
        super().__init__({
            'type': 'string',
            'format': 'time',
        }, validator, *args, **kwargs)


class DateTimeTyped(JSONTyped):
    """Wrap formencode validator with date-time type of JSON Schema"""
    def __init__(self, validator, *args, **kwargs):
        super().__init__({
            'type': 'string',
            'format': 'date-time',
        }, validator, *args, **kwargs)


class UUIDTyped(JSONTyped):
    """Wrap formencode validator with uuid type of JSON Schema"""
    def __init__(self, validator, *args, **kwargs):
        super().__init__({
            'type': 'string',
            'format': 'uuid',
        }, validator, *args, **kwargs)


class StringTyped(JSONTyped):
    """Wrap formencode validator with string type of JSON Schema"""
    def __init__(self, validator, *args, **kwargs):
        super().__init__({
            'type': 'string',
            'format': 'uuid',
        }, validator, *args, **kwargs)


class DecimalTyped(JSONTyped):
    """Wrap formencode validator with decimal type of JSON Schema"""
    def __init__(self, validator, *args, **kwargs):
        super().__init__({
            'type': 'number',
            'format': 'decimal',
        }, validator, *args, **kwargs)


class FloatTyped(JSONTyped):
    """Wrap formencode validator with float type of JSON Schema"""
    def __init__(self, validator, *args, **kwargs):
        super().__init__({
            'type': 'number',
            'format': 'float',
        }, validator, *args, **kwargs)


class IntegerTyped(JSONTyped):
    """Wrap formencode validator with integer type of JSON Schema"""
    def __init__(self, validator, *args, **kwargs):
        super().__init__({
            'type': 'integer',
        }, validator, *args, **kwargs)


class BooleanTyped(JSONTyped):
    """Wrap formencode validator with boolean type of JSON Schema"""
    def __init__(self, validator, *args, **kwargs):
        super().__init__({
            'type': 'boolean',
        }, validator, *args, **kwargs)
