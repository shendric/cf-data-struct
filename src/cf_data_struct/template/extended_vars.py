# -*- coding: utf-8 -*-
"""

"""

__author__ = "Stefan Hendricks <stefan.hendricks@awi.de>"


class StrExtendedFormatOptions(str):
    """
    A version of the built-in str class that supports additional formatting options.

    - Uppercase: Use the format specifier "upper" to convert the string to uppercase.
                 `"{:upper}".format(StrExtendedFormatOptions("my_string"))` will return `MY_STRING`.
    - Lowercase: Use the format specifier "lower" to convert the string to lowercase
                 `"{:lower}".format(StrExtendedFormatOptions("MY_STRING"))` will return `my_string`.
    """
    def __format__(self, format_spec: str) -> str:
        match format_spec:
            case "upper": return self.upper()
            case "lower": return self.lower()
            case _:  return f"{super().__format__(format_spec)}"