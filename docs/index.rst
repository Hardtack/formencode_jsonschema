formencode_jsonschema
=====================

formencode_jsonschema is a library that converts
`Formencode <http://www.formencode.org/en/latest/>`_ schema to
`JSON Schema <http://json-schema.org/>`_.
And it dependes on `Marshmallow <https://marshmallow.readthedocs.org/en/latest/>`_

Source code
-----------

Source codes are hosted on `Github <https://github.com/Hardtack/formencode_jsonschema>`_

How to use it
-------------

You can use it like this.

.. code-block:: python

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

User's Guide
------------

.. toctree::
   :maxdepth: 2

   converter
   typed

API References
--------------

.. toctree::

   api/modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

