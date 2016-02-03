Converter
=========

Formencode's validators can be converted to JSON Schema by
:mod:`formencode_jsonschema.converters`. It converts only validators whose type can be extracted.
Like ``UnicodeString``, ``Bool``, ``Int``, etc... and some wrapping validators.
