import pathlib
import uuid

from django.utils.text import slugify


def book_image_path(instance: "Book", filename: str) -> pathlib.Path:
    filename = (
        f"{slugify(instance.title)}-{uuid.uuid4()}" + pathlib.Path(filename).suffix
    )
    return pathlib.Path("upload/plays") / pathlib.Path(filename)
