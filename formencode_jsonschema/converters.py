import abc

from formencode import validators as v, compound
from formencode.api import Validator, NoDefault

from .typed import JSONTyped
from .utils import get_type_base


TYPE_MAPPING = {
    v.ByteString: bytes,
    v.StringBool: str,
    v.Bool: bool,
    v.Int: int,
    v.Number: float,
    v.UnicodeString: str,
    v.Regex: str,
}


class SchemaDelegate(object):
    def can_convert(self, validator: Validator):
        raise NotImplementedError

    def convert_validator(self, validator: Validator):
        raise NotImplementedError

    def is_required(self, validator: Validator):
        raise NotImplementedError


class ValidatorConverter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def can_convert(self, validator: Validator, delegate: SchemaDelegate):
        pass

    @abc.abstractmethod
    def convert(self, validator: Validator, delegate: SchemaDelegate):
        pass

    def is_required(self, validator: Validator, delegate: SchemaDelegate):
        if validator.not_empty:
            return True
        if validator.if_missing is NoDefault:
            return True
        return False


class SimpleValidatorConverter(ValidatorConverter):
    def __init__(self, validator_class, python_type):
        super().__init__()
        self.validator_class = validator_class
        self.python_type = python_type

    def can_convert(self, validator: Validator, delegate: SchemaDelegate):
        return isinstance(validator, self.validator_class)

    def convert(self, validator: Validator, delegate: SchemaDelegate):
        converted = get_type_base(self.python_type)
        assert converted is not None
        return converted


class TypedValidatorConverter(ValidatorConverter):
    def can_convert(self, validator: Validator, delegate: SchemaDelegate):
        return isinstance(validator, JSONTyped)

    def convert(self, validator: Validator, delegate: SchemaDelegate):
        return validator.json_type

    def is_required(self, validator: Validator, delegate: SchemaDelegate):
        if validator.required is not NoDefault:
            return validator.required
        return delegate.is_required(validator.validator)


class AllValidatorConverter(ValidatorConverter):
    def can_convert(self, validator: Validator, delegate: SchemaDelegate):
        if not isinstance(validator, compound.All):
            return False
        return delegate.can_convert(validator.validators[0])

    def convert(self, validator: Validator, delegate: SchemaDelegate):
        return delegate.convert_validator(validator.validators[0])

    def is_required(self, validator: Validator, delegate: SchemaDelegate):
        is_required = super().is_required
        return all(is_required(x, delegate) for x in validator.validators)


class PipeValidatorConverter(ValidatorConverter):
    def can_convert(self, validator: Validator, delegate: SchemaDelegate):
        if not isinstance(validator, compound.Pipe):
            return False
        return delegate.can_convert(validator.validators[-1])

    def convert(self, validator: Validator, delegate: SchemaDelegate):
        return delegate.convert_validator(validator.validators[-1])

    def is_required(self, validator: Validator, delegate: SchemaDelegate):
        is_required = super().is_required
        return all(is_required(x, delegate) for x in validator.validators)


SIMPLE_CONVERTERS = tuple(SimpleValidatorConverter(x, y)
                          for x, y in TYPE_MAPPING.items())

DEFAULT_CONVERTERS = SIMPLE_CONVERTERS + (
    TypedValidatorConverter(),
    AllValidatorConverter(),
    PipeValidatorConverter(),
)
