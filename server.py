#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class RobotRequestHandler(BaseHTTPRequestHandler):
    def is_valid_number(self, number: str) -> bool:
        try:
            float(number)
        except ValueError:
            return False
        return True

    def do_PUT(self):
        if self.path == "/api/v1/config/cameras":
            EXPECTED_KEYS = set(["ID", "Serial", "Type", "Gain"])
            EXPECTED_TYPES = ["TYPE_A", "TYPE_B"]

            content_len = int(self.headers.get("Content-Length"))
            try:
                body = json.loads(self.rfile.read(content_len))
            except json.JSONDecodeError:
                self.send_error(400, "Invalid request.")
                return

            unique_ids = set()
            unique_serials = set()

            for config in body:
                if config.keys() != EXPECTED_KEYS:
                    self.send_error(400, "Missing required fields.")
                    return

                if config["Type"] not in EXPECTED_TYPES:
                    self.send_error(400, "Invalid type.")
                    return

                if not self.is_valid_number(config["Gain"]):
                    self.send_error(400, "Invalid Gain value")
                    return

                unique_ids.add(config["ID"])
                unique_serials.add(config["Serial"])

            if len(unique_ids) != len(body):
                self.send_error(400, "Repeated IDs")
                return

            if len(unique_serials) != len(body):
                self.send_error(400, "Repeated serial number")
                return

            self.send_response(204)
            self.end_headers()


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8888), RobotRequestHandler)
    server.serve_forever()
