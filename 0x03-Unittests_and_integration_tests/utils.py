#!/usr/bin/env python3
"""
utils.py
Utility functions for nested map access, HTTP JSON retrieval, and memoization.
"""
from typing import Any, Mapping, Sequence, Callable
import requests


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access a nested object in nested_map with a sequence of keys."""
    current = nested_map
    for key in path:
        current = current[key]
    return current

def get_json(url: str) -> Any:
    """Get JSON from a URL."""
    response = requests.get(url)
    return response.json()

def memoize(method: Callable) -> property:
    """
    Decorator that turns a method into a memoized property.
    The method should take only 'self' as argument.
    """
    def wrapper(self):
        attr_name = f"_{method.__name__}_memoized"
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)
    return property(wrapper)
