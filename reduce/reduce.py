import json
import statistics
from helpers.validate_json import validate_json

SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "random_numbers": {"type": "array"},
        "treshold": {"type": "number"}
    },
    "required": ["title", "random_numbers", ]
}


def lambda_handler(event, context=None):
    """
    Handle an AWS Lambda function event.

    :param event: The event object containing information about the Lambda invocation.
                  It typically includes a 'body' field with a JSON payload.
    :param context: The Lambda execution context, which provides information about the runtime environment.
                   (Optional, defaults to None)

    :return: A dictionary with 'statusCode' and 'body' keys. The 'statusCode' indicates the HTTP status code
             of the Lambda response, and the 'body' contains the response content.
             If the input_data is valid, it returns a 200 status code and the JSON-encoded statistics summary in the
             response body. If there are validation errors or exceptions during execution,it returns a 400 status code
             with error messages or exception descriptions in the response body.
    """
    try:
        input_data = json.loads(event)
        is_valid, errors = validate_json(input_data, SCHEMA)
        result = calculate_summary_statistics(input_data)
        if not is_valid:
            return {
                'statusCode': 400,
                'body': json.dumps(errors)
            }
        return {
            'statusCode': 200,
            'body': json.dumps(
                {
                    "title": input_data.get("title"),
                    "statistics": result
                }
            )
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }


def calculate_summary_statistics(input_data):
    """
    Calculate summary statistics based on the input data containing random numbers and worker assignments.

    :param input_data: A dictionary containing the following key-value pairs:
        - 'title': The description of the data.
        - 'random_numbers': A list of tuples, each containing a worker identifier and a numeric value.
        - 'threshold' (optional): A numeric threshold for filtering values.

    :return: A dictionary containing summary statistics:
        - 'title': The description of the data.
        - 'Number of Samples Generated': The total number of samples.
        - 'Number of Samples greater or equal to Threshold': The number of samples meeting or exceeding the threshold.
        - 'Sum': The sum of all values.
        - 'Median': The median value of all values.
        - 'Minimum': The minimum value among all values.
        - 'Maximum': The maximum value among all values.
        - 'Count distinct worker, value pairs': The count of distinct worker-value pairs.

        For each worker, the function also calculates the same statistics and includes them in the result under the
        'Worker {worker_id} Statistics' key, where {worker_id} is the identifier of the worker.

    This function processes the input data to extract statistics related to both the entire dataset and each individual
    worker's dataset, providing a comprehensive summary of the data distribution.
    """
    random_numbers = input_data.get("random_numbers")
    threshold = input_data.get("threshold", 0)

    # create lists for total statistics
    workers = []
    values = []
    for worker, num in random_numbers:
        workers.append(worker)
        values.append(num)

    # get total stats
    stats = get_stats(threshold, values)

    # get stats for each worker
    for worker in workers:
        # get only worker values
        worker_values = [num for w, num in random_numbers if w == worker]
        stats[f'Worker {worker} Statistics'] = get_stats(threshold, worker_values)
    return stats


def get_stats(threshold, values):
    """
    Calculate summary statistics for a list of numeric values.

    :param threshold: The numeric threshold for filtering values.
    :type threshold: float or int

    :param values: A list of numeric values for which statistics will be calculated.
    :type values: list

    :return: A dictionary containing summary statistics:
        - 'Number of Samples Generated': The total number of samples.
        - 'Number of Samples greater or equal to Threshold': The number of samples meeting or exceeding the threshold.
        - 'Sum': The sum of all values.
        - 'Median': The median value of all values.
        - 'Minimum': The minimum value among all values.
        - 'Maximum': The maximum value among all values.
        - 'Count distinct worker, value pairs': The count of distinct pairs in the input.
    """
    stats = {
        'Number of Samples Generated': len(values),
        'Number of Samples greater or equal to Threshold': len(
            [num for num in values if num >= threshold]),
        'Sum': sum(values),
        'Median': statistics.median(values),
        'Minimum': min(values),
        'Maximum': max(values),
        'Count distinct worker, value pairs': len(values)
    }
    return stats
