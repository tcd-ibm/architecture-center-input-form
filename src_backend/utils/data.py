from typing import Any, TypeVar
from fastapi import Response


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

def calculate_number_of_pages(count: int, per_page: int) -> int:
    return count // per_page + (1 if count % per_page else 0)

def set_count_headers(response: Response, count: int, per_page: int) -> None:
    response.headers['X-Total-Count'] = str(count)
    response.headers['X-Total-Pages'] = str(calculate_number_of_pages(count, per_page))