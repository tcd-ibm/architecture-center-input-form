from typing import Callable
from io import BytesIO
import os
from PIL import Image


# TODO change the path parameters' type ?
# TODO exceptions and race condition handling
# TODO reading directory path from env

class FileStorageManager:
    def __init__(self, directory_path: str, verification_func: Callable[[bytes], bool]):
        self.directory_path = directory_path
        self.verification_func = verification_func
    

    def read_if_exists(self, relative_file_path: str) -> bytes | None:
        full_path = self.directory_path + relative_file_path

        if not os.path.exists(full_path):
            return None
        
        with open(full_path, 'rb') as file_handle:
            return file_handle.read()


    def write(self, relative_file_path: str, file_contents: bytes) -> None:
        if not self.verification_func(file_contents):
            raise FileValidationException()
        
        full_path = self.directory_path + relative_file_path
        
        with open(full_path, 'wb') as file_handle:
            file_handle.write(file_contents)


    def delete_if_exists(self, relative_file_path: str) -> None:
        full_path = self.directory_path + relative_file_path

        if os.path.exists(full_path):
            os.remove(full_path)


def verify_image(file_contents: bytes) -> bool:
    handle = BytesIO(file_contents)
    try:
        im = Image.open(handle)
        im.verify()
    except Exception:
        return False
    finally:
        im.close()
    return True


file_storage = FileStorageManager('./database/content/', verify_image)


class FileValidationException(Exception):
    def __init__(self, msg='File validation failed', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
