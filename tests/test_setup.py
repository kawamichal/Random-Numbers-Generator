import unittest
import json
from setup.setup import lambda_handler


class TestLambdaHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.valid_input_event = json.dumps(
            {"title": "Setup Handler Test", "n_workers": 4, "random_seed": 42, "n_sims": 100, "threshold": 0.5}
        )
        self.invalid_input_event = json.dumps(
            {"title": "Invalid Setup Handler Test", "n_workers": 3, "random_seed": 24, "threshold": 0.7}
        )

    def test_valid_input(self):
        response = lambda_handler(self.valid_input_event)
        response_data = json.loads(response['body'])

        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response_data, {
            "title": "Setup Handler Test",
            "n_workers": 4,
            "random_seed": 42,
            "n_sims": 100,
            "threshold": 0.5
        })

    def test_invalid_input(self):
        response = lambda_handler(self.invalid_input_event)
        response_data = json.loads(response['body'])

        self.assertEqual(response['statusCode'], 400)
        self.assertIn("'n_sims' is required", response_data)
