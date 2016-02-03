formencode_jsonschema
=====================

Converts [formencode](http://www.formencode.org/en/latest/)'s schema to
[JSON Schema](http://json-schema.org/)
using [Marshmallow](https://marshmallow.readthedocs.org/en/latest/).

How to use it
-------------

You can use it like this.

```python
>>> from myproject.schemas import SomeFormencodeSchema
>>> from formencode_jsonschema import JSONSchema
>>> json_schema = JSONSchema()
>>> formencode_schema = SomeFormencodeSchema()
>>> result = json_schema.dump(formencode_schema)
>>> result.data
{
	"type": "object",
	"required": ["foo", ...],
    "properties": {
    	"foo": {
        	"type": "string"
        },
        "bar": ...
    }
}
```

Typed validator
---------------

You can explicitly define validator as JSON typed validator.

```python
from formencode import Schame, validators as v
from formencode_jsonschema import typed, JSONSchema


class SomeFormencodeSchema(Schema):
    foo = typed.BooleanTyped(v.UnicodeString(), required=False)
    bar = typed.JSONTyped({
    	"type": "string",
    }, v.Int())
```

```python
>>> json_schema = JSONSchema()
>>> formencode_schema = SomeFormencodeSchema()
>>> result = json_schema.dump(formencode_schema)
>>> result.data
{
	"type": "object",
	"required": ["bar"],
    "properties": {
    	"foo": {
        	"type": "boolean"
        },
        "bar": {
        	"type": "string"
        }
    }
}
```
