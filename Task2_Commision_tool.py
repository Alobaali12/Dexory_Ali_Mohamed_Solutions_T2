"""
Author: Ali Mohamed
Date: 18/07/2025
Description:
    This script provides a command-line tool to commission scanning cameras 
    on a robot by configuring them via a local API. It prompts the user for 
    camera type and the path to a JSON file containing serial numbers, 
    then constructs a configuration payload and sends it to the API endpoint.
"""

import json
import requests
import os

API_URL = "http://localhost:8888/api/v1/config/cameras" 
GAIN_VALUE = 20.0
VALID_TYPES = ["TYPE_A", "TYPE_B"]

def get_camera_type():
    while True:
        print("Select camera type:")
        print("1. TYPE_A")
        print("2. TYPE_B")
        choice = input("Enter choice (1 or 2): ").strip()
        if choice == "1":
            return "TYPE_A"
        elif choice == "2":
            return "TYPE_B"
        print("Invalid selection. Please choose 1 or 2.")

def get_serial_numbers(filepath):
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, 'r') as f:
        data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError("Expected a dictionary of serial numbers.")
        return data

def build_configuration(camera_type, serials_dict):
    config = []
    for camera_id, serial in serials_dict.items():
        config.append({
            "ID": camera_id,
            "Serial": serial,
            "Type": camera_type,
            "Gain": GAIN_VALUE
        })
    return config

def send_configuration(config):
    response = requests.put(API_URL, json=config)
    if response.status_code == 204:
        print("Cameras successfully configured!")
        return True
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return False


def main():
    try:
        camera_type = get_camera_type()
        json_path = input("Enter path to serial_numbers.json: ").strip()
        serials = get_serial_numbers(json_path)
        config = build_configuration(camera_type, serials)
        send_configuration(config)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
