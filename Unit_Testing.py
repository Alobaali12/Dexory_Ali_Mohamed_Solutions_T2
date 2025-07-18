import unittest
from unittest.mock import patch, MagicMock
import json

import Task2_Commision_tool

class TestBuildConfiguration(unittest.TestCase):
    def test_build_configuration(self):
        camera_type = "TYPE_B"
        serials = {"A": "X1", "B": "Y2", "C": "Z3"}
        config = Task2_Commision_tool.build_configuration(camera_type, serials)
        self.assertEqual(len(config), 3)
        # Check each entry
        ids = {entry["ID"] for entry in config}
        self.assertSetEqual(ids, set(serials.keys()))
        for entry in config:
            self.assertEqual(entry["Type"], camera_type)
            self.assertEqual(entry["Gain"], Task2_Commision_tool.GAIN_VALUE)
            self.assertEqual(entry["Serial"], serials[entry["ID"]])

class TestSendConfiguration(unittest.TestCase):
    @patch("Task2_Commision_tool.requests.put")
    def test_send_success(self, mock_put):
        # Simulate 204 No Content (success)
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_put.return_value = mock_response

        config = [{"ID": "A", "Serial": "X", "Type": "TYPE_A", "Gain": 20.0}]
        result = Task2_Commision_tool.send_configuration(config)
        self.assertTrue(result)  # Should indicate success
        mock_put.assert_called_once_with(
            Task2_Commision_tool.API_URL,
            json=config
        )

    @patch("Task2_Commision_tool.requests.put")
    def test_send_failure(self, mock_put):
        # Simulate non-204 failure
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad request"
        mock_put.return_value = mock_response

        config = [{"ID": "A", "Serial": "X", "Type": "TYPE_A", "Gain": 20.0}]
        result = Task2_Commision_tool.send_configuration(config)
        self.assertFalse(result)  # Should indicate failure
        mock_put.assert_called_once()

class TestGetSerialNumbers(unittest.TestCase):
    def setUp(self):
        self.valid_file = "temp_serials.json"
        with open(self.valid_file, "w") as f:
            json.dump({"A": "X", "B": "Y"}, f)

    def tearDown(self):
        import os
        os.remove(self.valid_file)

    def test_valid_serials(self):
        data = Task2_Commision_tool.get_serial_numbers(self.valid_file)
        self.assertEqual(data, {"A": "X", "B": "Y"})

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            Task2_Commision_tool.get_serial_numbers("nonexistent.json")

    def test_invalid_format(self):
        bad_file = "bad.json"
        with open(bad_file, "w") as f:
            json.dump(["not", "a", "dict"], f)
        with self.assertRaises(ValueError):
            Task2_Commision_tool.get_serial_numbers(bad_file)
        import os; os.remove(bad_file)

if __name__ == "__main__":
    unittest.main()
