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
    """Interface for delegating validator conversion to schema."""
    def can_convert(self, validator: Validator):
        raise NotImplementedError

    def convert_validator(self, validator: Validator):
        raise NotImplementedError

    def is_required(self, validator: Validator):
        raise NotImplementedError


class ValidatorConverter(metaclass=abc.ABCMeta):
    """Base class for validator converters."""
    @abc.abstractmethod
    def can_convert(self, validator: Validator, delegate: SchemaDelegate):
        """Check acceptability."""
        pass

    @abc.abstractmethod
    def convert(self, validator: Validator, delegate: SchemaDelegate):
        """Excute conversion."""
        pass

    def is_required(self, validator: Validator, delegate: SchemaDelegate):
        """Get required flag from validator."""
        if validator.not_empty:
            return True
        if validator.if_missing is NoDefault:
            return True
        return False


class SimpleValidatorConverter(ValidatorConverter):
    """
    Simple converter that convert specific validator into specific python type
    and, convert it to json schema

    """
    def __init__(self, validator_class, python_type):
        """
        :param validator_class: base class of target validator.
        :param python_type: python type to be converted. should be in
                            ``TYPE_MAP`` in :mod:`formencode_jsonschema.utils`
        
        """
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
    """
    Convert validator that wraped by typed validator.
    """
    def can_convert(self, validator: Validator, delegate: SchemaDelegate):
        return isinstance(validator, JSONTyped)

    def convert(self, validator: Validator, delegate: SchemaDelegate):
        json_schema_type = (validator.json_type or {}).copy()
        if validator.description is not None:
            json_schema_type['description'] = validator.description
        return json_schema_type

    def is_required(self, validator: Validator, delegate: SchemaDelegate):
        if validator.required is not NoDefault:
            return validator.required
        return delegate.is_required(validator.validator)


class AllValidatorConverter(ValidatorConverter):
    """
    Convert ``All`` validator using first validator.
    """
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
    """
    Convert ``All`` validator using last validator.
    """
    def can_convert(self, validator: Validator, delegate: SchemaDelegate):
        if not isinstance(validator, compound.Pipe):
            return False
        return delegate.can_convert(validator.validators[-1])

    def convert(self, validator: Validator, delegate: SchemaDelegate):
        return delegate.convert_validator(validator.validators[-1])

    def is_required(self, validator: Validator, delegate: SchemaDelegate):
        is_required = super().is_required
        return all(is_required(x, delegate) for x in validator.validators)

#: Define simple converters
SIMPLE_CONVERTERS = tuple(SimpleValidatorConverter(x, y)
                          for x, y in TYPE_MAPPING.items())

#: Default converters
DEFAULT_CONVERTERS = SIMPLE_CONVERTERS + (
    TypedValidatorConverter(),
    AllValidatorConverter(),
    PipeValidatorConverter(),
)
