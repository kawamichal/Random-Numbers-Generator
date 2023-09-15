import json
import multiprocessing
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


def single_worker_generate_random_numbers(worker_id, worker_sims, result_queue, random_seed):
    """
    Generate random numbers for a single worker.

    :param worker_id: Unique identifier for the worker.
    :type worker_id: int

    :param worker_sims: Number of random numbers to generate for the worker.
    :type worker_sims: int

    :param result_queue: A multiprocessing queue to store the generated random numbers.
    :type result_queue: multiprocessing.Queue

    :param random_seed: The random seed for deterministic behavior.
    :type random_seed: int

    :return: None
    """
    # Set the random seed for deterministic behavior
    random.seed(random_seed + worker_id)
    worker_numbers = [(worker_id, random.random()) for _ in range(worker_sims)]
    # Put the results in queue
    result_queue.put(worker_numbers)


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
    # Divide the task among worker processes
    sims_per_worker = n_sims // n_workers
    remainder = n_sims % n_workers

    # Create a multiprocessing queue to collect results from workers
    result_queue = multiprocessing.Queue()

    # Create a list to hold references to worker processes
    processes = []

    # simulating the workers
    for worker_id in range(n_workers):
        worker_sims = sims_per_worker

        # handling the remainder simulations
        if remainder:
            worker_sims += 1
            remainder -= 1

        process = multiprocessing.Process(target=single_worker_generate_random_numbers,
                                          args=(worker_id, worker_sims, result_queue, random_seed))
        processes.append(process)
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

    random_numbers = []
    for _ in range(n_workers):
        result = result_queue.get()
        random_numbers.extend(result)

    return random_numbers
