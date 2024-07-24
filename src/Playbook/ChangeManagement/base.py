from typing import Any

def create_instance(cls, *args, **kwargs):
    """Helper function to create instances of classes."""
    return cls(*args, **kwargs)

class BaseClass:
    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)