from enum import Enum


class RegExEnum(Enum):
    BRAND = (
        r'^[A-Z][a-zA-Z\d]{1,24}$',
        'First letter uppercase min 2 max 24 ch'
    )

    EMAIL = (
        r'^[\w.%+-]+@gmail\.com$',
        'The email domain must be gmail.com'
    )

    NAME = (
        r'^[А-ЯЁІЇЄ][а-яёіїґє]{1,49}$',
        'This name must contain only Cyrillic characters.'
    )

    SURNAME = (
        r'^[А-ЯЁІЇЄ][а-яёіїґє]{1,49}$',
        'This surname must contain only Cyrillic characters.'
    )

    PASSWORD = (
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\'`\!@#$%\^&\*\(\)\-_=\+\|\\\/\?\.>,<])(?=.*\S)'
        r'[a-zA-Z\d\'`\!@#$%\^&\*\(\)\-_=\+\|\\\/\?\.>,<]{8,30}$',
        'This password must be at least one uppercase letter, at least one lowercase letter, '
        'at least one special character and at least one number min 8 max 30 characters.'
    )

    def __init__(self, pattern: str, msg: str | list[str]):
        self.pattern = pattern
        self.msg = msg
