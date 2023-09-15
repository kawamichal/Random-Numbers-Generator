import unittest
import json
from map.map import lambda_handler


class TestLambdaHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.input_event = json.dumps(
            {"title": "Map Handler Test", "n_workers": 3, "random_seed": 2, "n_sims": 10, "threshold": 0.1}
        )

    def test_deterministic_results(self):
        response1 = lambda_handler(self.input_event)
        response_data1 = json.loads(response1['body'])["random_numbers"]

        response2 = lambda_handler(self.input_event)
        response_data2 = json.loads(response2['body'])["random_numbers"]

        self.assertEqual(response1['statusCode'], 200)
        self.assertEqual(response2['statusCode'], 200)
        self.assertEqual(response_data1, response_data2)
