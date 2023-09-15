def validate_json(json_data, schema):
    """
    Validate a JSON object against a JSON schema.

    :param json_data: The JSON object to validate.
    :param schema: The JSON schema to use for validation. The schema should be a dictionary that may include:
        - 'required' (optional): A list of required property names.
        - 'properties': A dictionary mapping property names to their respective schemas.
          Each property schema may include a 'type' key indicating the expected data type (e.g., 'string', 'integer',
          'number', 'array').

    :return: A tuple containing a boolean indicating whether the JSON data is valid according to the schema
             and a list of validation error messages.
    """
    errors = []

    # Check if the JSON data is an object
    if not isinstance(json_data, dict):
        errors.append("Object is not a valid JSON.")
        return False, errors

    # Check if all required properties are present
    for required_property in schema.get("required", []):
        if required_property not in json_data:
            errors.append(f"'{required_property}' is required")

    # Check property types
    type_mapping = {
        "string": str,
        "integer": int,
        "number": (int, float),
        "array": list,
    }
    for property_name, property_schema in schema.get("properties", {}).items():
        if property_name in json_data:
            property_value = json_data[property_name]
            property_type = property_schema.get("type")

            if not isinstance(property_value, type_mapping.get(property_type)):
                errors.append(f"'{property_name}' should be of type '{property_type}'")

    if errors:
        return False, errors

    return True, []
