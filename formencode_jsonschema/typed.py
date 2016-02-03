from formencode.api import FancyValidator, NoDefault


class JSONTyped(FancyValidator):
    __unpackargs__ = ('json_type', 'validator')

    def __init__(self, json_type, validator, *args, **kwargs):
        self.json_type = json_type
        self.validator = validator
        self.required = kwargs.pop('required', NoDefault)
        super().__init__(*args, **kwargs)

    def _convert_to_python(self, value, state=None):
        return self.validator.to_python(value, state)

    def _convert_from_python(self, value, state=None):
        return self.validator.from_python(value, state)


class ObjectTyped(JSONTyped):
    def __init__(self, validator, *args, **kwargs):
        super().__init__({
            'type': 'object',
        }, validator, *args, **kwargs)


class ArrrayTyped(JSONTyped):
    def __init__(self, validator, *args, **kwargs):
        super().__init__({
            'type': 'array',
        }, validator, *args, **kwargs)


class DateTyped(JSONTyped):
    def __init__(self, validator, *args, **kwargs):
        super().__init__({
            'type': 'string',
            'format': 'date',
        }, validator, *args, **kwargs)


class TimeTyped(JSONTyped):
    def __init__(self, validator, *args, **kwargs):
        super().__init__({
            'type': 'string',
            'format': 'time',
        }, validator, *args, **kwargs)


class DateTimeTyped(JSONTyped):
    def __init__(self, validator, *args, **kwargs):
        super().__init__({
            'type': 'string',
            'format': 'date-time',
        }, validator, *args, **kwargs)


class UUIDTyped(JSONTyped):
    def __init__(self, validator, *args, **kwargs):
        super().__init__({
            'type': 'string',
            'format': 'uuid',
        }, validator, *args, **kwargs)


class StringTyped(JSONTyped):
    def __init__(self, validator, *args, **kwargs):
        super().__init__({
            'type': 'string',
            'format': 'uuid',
        }, validator, *args, **kwargs)


class DecimalTyped(JSONTyped):
    def __init__(self, validator, *args, **kwargs):
        super().__init__({
            'type': 'number',
            'format': 'decimal',
        }, validator, *args, **kwargs)


class FloatTyped(JSONTyped):
    def __init__(self, validator, *args, **kwargs):
        super().__init__({
            'type': 'number',
            'format': 'float',
        }, validator, *args, **kwargs)


class IntegerTyped(JSONTyped):
    def __init__(self, validator, *args, **kwargs):
        super().__init__({
            'type': 'number',
            'format': 'integer',
        }, validator, *args, **kwargs)


class BooleanTyped(JSONTyped):
    def __init__(self, validator, *args, **kwargs):
        super().__init__({
            'type': 'boolean',
        }, validator, *args, **kwargs)
