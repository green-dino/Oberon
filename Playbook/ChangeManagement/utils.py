from typing import Any, Type

def create_instance(cls: Type[Any], *args: Any, **kwargs: Any) -> Any:
    return cls(*args, **kwargs)
