from flask_marshmallow.schema import Schema


def validate_schema_unknown_fields(schema: Schema, data: dict):
    """ Validates if in data there are fields not present
        or dump_only=True in Schema

        - schema (flask_marshmallow.schema.Schema): Instance of Schema
        - data (dict): Data to validate

    """
    errors = {}
    for field in data:
        if (field not in schema.declared_fields) or (
                schema.declared_fields[field].dump_only):
            errors[field] = ['Unknown field']
    return errors
