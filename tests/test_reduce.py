import unittest
import json
from map.map import lambda_handler as map_lambda_handler
from reduce.reduce import lambda_handler as reduce_lambda_handler


class TestLambdaHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.input_event = json.dumps(
            {"title": "Map Handler Test", "n_workers": 3, "random_seed": 2, "n_sims": 5, "threshold": 0.6}
        )

    def test_reduce_lambda(self):
        map_response = map_lambda_handler(self.input_event)
        map_response_data = map_response['body']
        self.assertEqual(map_response['statusCode'], 200)

        reduce_response = reduce_lambda_handler(map_response_data)
        reduce_response_stats = json.loads(reduce_response.get("body")).get("statistics")
        self.assertEqual(reduce_response['statusCode'], 200)

        # example tests
        self.assertIn("Worker 2 Statistics", reduce_response_stats)
        self.assertEqual(reduce_response_stats.get("Maximum"), 0.9560342718892494)

