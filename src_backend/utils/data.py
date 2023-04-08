from typing import Any, TypeVar, Type


T = TypeVar('T')

def patch_object(instance: T, patch: Any) -> T:
    for k, v in patch.__dict__.items():
        if v is not None:
            setattr(instance, k, v)

    return instance