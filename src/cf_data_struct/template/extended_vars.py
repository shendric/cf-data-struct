# -*- coding: utf-8 -*-
"""

"""

__author__ = "Stefan Hendricks <stefan.hendricks@awi.de>"

import re


class StrExtendedFormatOptions(str):
    """
    A version of the built-in str class that supports additional formatting options.

    - Uppercase: "^" to convert the string to uppercase.
                 `"{:^}".format(StrExtendedFormatOptions("my_string"))` will return `MY_STRING`.
    - Lowercase: "v" to convert the string to lowercase
                 `"{:v}".format(StrExtendedFormatOptions("MY_STRING"))` will return `my_string`.
    - Identifier: "i" to make a string a valid identifier.
                  `[:i}.format(StrExtendedFormatOptions("My String - 1"))` will return `My_String___1'`.
    - Identifier Uppercase: "i^" to make a string a valid identifier, but uppercase.
                  `[:i^}.format(StrExtendedFormatOptions("My String - 1"))` will return `MY_STRING___1'`.
    - Identifier Lowercase: "iv" to make a string a valid identifier, but lowercase.
                  `[:i^}.format(StrExtendedFormatOptions("My String - 1"))` will return `my_string___1'`.
    """
    def __format__(self, format_spec: str) -> str:
        match format_spec:
            case "^": return self.upper()
            case "v": return self.lower()
            case "i": return to_identifier(self)
            case "i^": return to_identifier(self).upper()
            case "iv": return to_identifier(self).lower()
            case _:  return f"{super().__format__(format_spec)}"


def to_identifier(string_value: str) -> str:
    """
    Convert a string to an identifier.
    (from https://stackoverflow.com/a/3305731)

    :param string_value: Any string

    :return: Converted string
    """
    return re.sub(r"\W|^(?=\d)", "_", string_value)