from typing import Any, TypeVar, Type


T = TypeVar('T')

def patch_object(instance: T, patch: Any) -> T:
    for k, v in patch.__dict__.items():
        if v is not None:
            setattr(instance, k, v)

    return instance

def is_empty(object: Any) -> bool:
    for k, v in object.__dict__.items():
        if v is not None:
            return False
        
    return True