"""
client.py
This module contains the Client class for integration testing.
"""

class Client:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def process(self, data):
        # Simulate processing data
        return f"Processed {data} for {self.name}"
