import re
from django.core.exceptions import ValidationError


def author_validate(author_name:str) -> None:
    pattern = '[A-Za-zА-Яа-яёЁ]+(?:-?[A-Za-zА-Яа-яёЁ]+)*(?: [A-Za-zА-Яа-яёЁ]+(?:-?[A-Za-zА-Яа-яёЁ]+)*){0,2}$'

    if not re.fullmatch(pattern=pattern, string=author_name):
        raise ValidationError('Введите корректное имя автора! Оно должно содержать только буквы и пробелы! А так же дефис, если фамилия двойная.')

