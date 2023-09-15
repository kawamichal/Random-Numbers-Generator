import json
from setup.setup import lambda_handler as setup_lambda_name
from map.map import lambda_handler as map_lambda_name
from reduce.reduce import lambda_handler as reduce_lambda_name

# Sample input data
example_input_data = json.dumps(
    {
        "title": "Random Number Generator",
        "n_workers": 4,
        "random_seed": 2,
        "n_sims": 9,
        "threshold": 0.6
    }
)


# Helper function to invoke Lambda functions
def invoke_lambda(lambda_name, input_payload):
    result = lambda_name(input_payload)
    return result


if __name__ == "__main__":
    while True:
        print("Hello! Type in your JSON. If you want to use one of my finest examples instead, type 'y'.")
        answer = input()
        if answer == "y":
            input_payload = example_input_data
        else:
            input_payload = answer

        # Step 1: Setup Lambda
        setup_response = invoke_lambda(setup_lambda_name, input_payload)
        print("Step 1: Setup Response")
        print(setup_response)

        if setup_response["statusCode"] == 200:
            # Step 2: Map Lambda
            map_response = invoke_lambda(map_lambda_name, setup_response['body'])
            print("Step 2: Map Response")
            print(map_response)

            if map_response["statusCode"] == 200:
                # Step 3: Reduce Lambda
                reduce_response = invoke_lambda(reduce_lambda_name, map_response['body'])
                print("Step 3: Reduce Response")
                print(reduce_response)

        print("")
        print("Type 'y' if you want to go again or anything else to quit.")
        go_again = input()
        if not go_again == "y":
            print("Bye!")
            break

