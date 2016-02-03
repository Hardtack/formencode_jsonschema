from marshmallow import Schema, fields
from formencode.api import Validator as FormencodeValidator
from formencode.schema import Schema as FormencodeSchema

from .converters import DEFAULT_CONVERTERS, SchemaDelegate


class JSONSchema(Schema, SchemaDelegate):
    """
    Marshmallow schema for convert Formencode's schema to JSON schema.

    You can add more converters by overriding ``__validator_converters__``
    field.

    """
    type = fields.Constant('object')
    properties = fields.Method('get_properties')
    required = fields.Method('get_required')

    __validator_converters__ = DEFAULT_CONVERTERS

    def get_required(self, schema: FormencodeSchema):
        fields = schema.fields
        required = []
        for name, validator in fields.items():
            if self.is_required(validator):
                required.append(name)
        return required

    def get_properties(self, schema: FormencodeSchema):
        fields = schema.fields
        properties = {}
        for name, validator in fields.items():
            properties[name] = self.convert_validator(validator)
        return properties

    def handle_unknown_validator(self, validator: FormencodeValidator):
        """When schema found unknown validator, handle that here."""
        raise ValueError(
            "Can not convert a validator {validator!r}"
            .format(validator=validator))

    # Delegate implementations

    def can_convert(self, validator: FormencodeValidator):
        for converter in self.__validator_converters__:
            if converter.can_convert(validator, self):
                return True
        return False

    def is_required(self, validator: FormencodeValidator):
        for converter in self.__validator_converters__:
            if converter.can_convert(validator, self) and \
                    converter.is_required(validator, self):
                return True
        return False

    def convert_validator(self, validator: FormencodeValidator):
        for converter in self.__validator_converters__:
            if converter.can_convert(validator, self):
                return converter.convert(validator, self)
        return self.handle_unknown_validator(validator)
