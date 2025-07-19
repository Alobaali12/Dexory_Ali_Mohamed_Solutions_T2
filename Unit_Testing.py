"""
Author: Ali Mohamed
Date: 18/07/2025
Description:
    This module contains unit tests for the camera commissioning tool
    implemented in `Task2_Commision_tool.py`. It verifies the correct
    behavior of the following functions:
    
    - build_configuration: Assembles camera configurations from serials
    - send_configuration: Sends configuration via HTTP PUT request
    - get_serial_numbers: Loads serial numbers from a JSON file
    
    Mocks are used for HTTP interactions to ensure tests run in isolation.
"""

import unittest
from unittest.mock import patch, MagicMock
import json
import os

import Task2_Commision_tool


class TestBuildConfiguration(unittest.TestCase):
    def test_build_configuration(self):
        camera_type = "TYPE_B"
        serials = {"A": "X1", "B": "Y2", "C": "Z3"}
        config = Task2_Commision_tool.build_configuration(camera_type, serials)
        self.assertEqual(len(config), 3)
        ids = {entry["ID"] for entry in config}
        self.assertSetEqual(ids, set(serials.keys()))
        for entry in config:
            self.assertEqual(entry["Type"], camera_type)
            self.assertEqual(entry["Gain"], Task2_Commision_tool.GAIN_VALUE)
            self.assertEqual(entry["Serial"], serials[entry["ID"]])
        print("Test build_configuration: PASS")


class TestSendConfiguration(unittest.TestCase):
    @patch("Task2_Commision_tool.requests.put")
    def test_send_success(self, mock_put):
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_put.return_value = mock_response

        config = [{"ID": "A", "Serial": "X", "Type": "TYPE_A", "Gain": 20.0}]
        result = Task2_Commision_tool.send_configuration(config)
        self.assertTrue(result)
        mock_put.assert_called_once_with(Task2_Commision_tool.API_URL, json=config)
        print("Test send_success: PASS")

    @patch("Task2_Commision_tool.requests.put")
    def test_send_failure(self, mock_put):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad request"
        mock_put.return_value = mock_response

        config = [{"ID": "A", "Serial": "X", "Type": "TYPE_A", "Gain": 20.0}]
        result = Task2_Commision_tool.send_configuration(config)
        self.assertFalse(result)
        mock_put.assert_called_once()
        print("Test send_failure: PASS")


class TestGetSerialNumbers(unittest.TestCase):
    def setUp(self):
        self.valid_file = "temp_serials.json"
        with open(self.valid_file, "w") as f:
            json.dump({"A": "X", "B": "Y"}, f)

    def tearDown(self):
        if os.path.exists(self.valid_file):
            os.remove(self.valid_file)
        if os.path.exists("bad.json"):
            os.remove("bad.json")

    def test_valid_serials(self):
        data = Task2_Commision_tool.get_serial_numbers(self.valid_file)
        self.assertEqual(data, {"A": "X", "B": "Y"})
        print("Test valid_serials: PASS")

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            Task2_Commision_tool.get_serial_numbers("nonexistent.json")
        print("Test missing_file: PASS")

    def test_invalid_format(self):
        with open("bad.json", "w") as f:
            json.dump(["not", "a", "dict"], f)
        with self.assertRaises(ValueError):
            Task2_Commision_tool.get_serial_numbers("bad.json")
        print("Test invalid_format: PASS")


if __name__ == "__main__":
    unittest.main()
