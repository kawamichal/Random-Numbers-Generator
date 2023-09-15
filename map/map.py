import json
import random


def lambda_handler(event, context=None):
    """
    Handle an AWS Lambda function event by generating random numbers based on input parameters.

    :param event: Event object that holds the input_data as a JSON payload.
    :type event: dict

    :param context: Object that provides methods and properties that offer information about the invocation,
                    function, and execution environment. (Optional, defaults to None)
    :type context: dict

    :returns: A dictionary containing a response with a status code and body, including the following fields:
        - "title": A descriptive title provided in the input_data.
        - "random_numbers": A JSON-encoded list of generated random numbers.
        - "threshold": The numeric threshold for the random numbers, defaults to 0 if not provided.
    :rtype: dict

    This Lambda function processes the input_data from the event object and generates random numbers based on the
    provided parameters (n_sims, random_seed, and n_workers). It returns a response containing the title,
    generated random numbers, and the threshold as specified above. If an exception is encountered during execution,
    it returns a response with a 400 status code and an error message.
    """

    try:
        input_data = json.loads(event)
        random_numbers = generate_random_numbers(
            input_data['n_sims'],
            input_data['random_seed'],
            input_data['n_workers']
        )
        return {
            'statusCode': 200,
            'body': json.dumps(
                {
                    "title": input_data.get("title"),
                    "random_numbers": random_numbers,
                    "threshold": input_data.get("threshold") or 0
                }
            )
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }


def generate_random_numbers(n_sims, random_seed, n_workers):
    """
    Generate random numbers distributed among workers.

    :param n_sims: The total number of simulations to be distributed among workers.
    :type n_sims: int

    :param random_seed: The seed for the random number generator to ensure reproducibility.
    :type random_seed: int

    :param n_workers: The number of workers or processes to distribute the simulations.
    :type n_workers: int

    :return: A list of tuples representing random numbers generated for each worker.
             Each tuple contains a worker identifier and a list of random numbers.
    :rtype: list

    This function distributes the simulations among workers, ensuring that each worker
    gets roughly an equal number of simulations. The total number of simulations may not be perfectly divisible
    by the number of workers, so some workers may get an additional simulation (remainder)
    to ensure all simulations are utilized.
    """
    random.seed(random_seed)
    sims_per_worker = n_sims // n_workers
    remainder = n_sims % n_workers

    random_numbers = []

    # simulating the workers
    for worker_id in range(n_workers):
        worker_sims = sims_per_worker

        # handling the remainder simulations
        if remainder:
            worker_sims += 1
            remainder -= 1

        # generating numbers for each worker
        worker_numbers = [random.random() for _ in range(worker_sims)]
        random_numbers.extend([(worker_id, num) for num in worker_numbers])

    return random_numbers
