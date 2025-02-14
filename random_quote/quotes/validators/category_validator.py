import re
from django.core.exceptions import ValidationError


def category_validate(category_name: str) -> None:
    pattern = "[A-Za-zА-Яа-яёЁ]+(?: [A-Za-zА-Яа-яёЁ]+)*(?: *, *[A-Za-zА-Яа-яёЁ]+(?: [A-Za-zА-Яа-яёЁ]+)*){0,7}$"

    if not re.fullmatch(pattern=pattern, string=category_name):
        raise ValidationError(
            "Введите корректное название категорий! Они могут содержать только буквы и пробелы,\
                               а так же должны разделяться запятыми! Их может быть не более 7 штук!"
        )
