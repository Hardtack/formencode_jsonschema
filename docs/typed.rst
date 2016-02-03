JSON Typed Validators
=====================

You can specify JSON Schema type using :mod:`formencode_jsonschema.typed`. ::

    from formencode import validators as v
    from formencode.schema import Schema
    from formencode_jsoncschema import typed

    from .validators import Password

    class UserCreate(Schema):
        username = v.PlainText(not_empty=True)
        password = typed.StringTyped(Password(), required=True)
        description = typed.JSONTyped({
            'type': 'string',
            'description': 'This is description',
        }, v.UnicodeString())
        birthday = typed.DateTyped(
            v.UnicodeString(),
            description="Description can be written at here")

You can find more types at :mod:`formencode_jsonschema.typed` API references.
