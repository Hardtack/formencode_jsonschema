from formencode import Schema, validators as v, compound

from formencode_jsonschema import JSONSchema, typed

from .utils import compare_schema


def test_simple_dump():
    class UserCreate(Schema):
        username = v.PlainText(not_empty=True)
        name = v.UnicodeString(not_empty=True)
        description = v.UnicodeString(if_missing=None)
        password = v.PlainText(not_empty=True)

    json_schema = JSONSchema()
    formencode_schema = UserCreate()

    result = json_schema.dump(formencode_schema)
    compare_schema({
        'required': ['name', 'password', 'username'],
        'type': 'object',
        'properties': {
            'username': {
                'type': 'string'
            },
            'name': {
                'type': 'string'
            },
            'description': {
                'type': 'string'
            },
            'password': {
                'type': 'string'
            }
        }
    }, result.data)


def test_compound_dump():
    class UserDescribe(Schema):
        name = compound.All(
            v.UnicodeString(not_empty=True),
            v.PlainText(),
        )
        description = v.UnicodeString(if_missing=None)

    json_schema = JSONSchema()
    formencode_schema = UserDescribe()

    result = json_schema.dump(formencode_schema)
    compare_schema({
        'required': ['name'],
        'type': 'object',
        'properties': {
            'name': {
                'type': 'string'
            },
            'description': {
                'type': 'string'
            }
        }
    }, result.data)


def test_typed_dump():
    class UserReally(Schema):
        really = typed.BooleanTyped(v.UnicodeString(if_missing=None),
                                    required=True)

    json_schema = JSONSchema()
    formencode_schema = UserReally()

    result = json_schema.dump(formencode_schema)
    compare_schema({
        'required': ['really'],
        'type': 'object',
        'properties': {
            'really': {
                'type': 'boolean'
            }
        }
    }, result.data)
