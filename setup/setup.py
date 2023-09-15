import json
from helpers.validate_json import validate_json

# Custom JSON schema
SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "n_workers": {"type": "integer"},
        "random_seed": {"type": "number"},
        "n_sims": {"type": "integer"},
        "treshold": {"type": "number"}
    },
    "required": ["title", "n_workers", "random_seed", "n_sims"]
}


def lambda_handler(event, context=None):
    """
    Handle an AWS Lambda function event by processing input JSON data.

    :param event: Event object that holds the input_data.
    :type event: str

    :param context: Object that provides methods and properties that offer information about the invocation,
                    function, and execution environment. (Optional, defaults to None)
    :type context: dict

    :returns: A dictionary containing a response with a status code and body, including the following fields:
        - "statusCode": The HTTP status code of the Lambda response.
        - "body": A JSON-encoded representation of the input_data if valid, or error messages if validation fails.
    :rtype: dict

    This Lambda function processes the input_data from the event object, attempts to validate it using a predefined
    schema (SCHEMA), and returns a response. If the input_data is valid, it returns a 200 status code and the
    JSON-encoded input_data in the response body. If there are validation errors or exceptions during execution,
    it returns a 400 status code with error messages.
    """
    try:
        input_data = json.loads(event)
        is_valid, errors = validate_json(input_data, SCHEMA)
        if not is_valid:
            return {
                'statusCode': 400,
                'body': json.dumps(errors)
            }
        return {
            'statusCode': 200,
            'body': json.dumps(input_data)
        }
    except Exception:
        return {
            'statusCode': 400,
            'body': ["The provided data is not in a JSON"]
        }
