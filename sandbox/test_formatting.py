# -*- coding: utf-8 -*-
"""

"""

__author__ = "Stefan Hendricks <stefan.hendricks@awi.de>"

from datetime import datetime

#
class StringExtendedFormatOptions(str):

    def __format__(self, format_spec: str) -> str:
        match format_spec:
            case "upper": return self.upper()
            case "lower": return self.lower()
            case _:  return f"{super().__format__(format_spec)}"

if __name__ == "__main__":

    # a = StringExtendedFormatOptions("Hello, World!")
    # print("{d:upper}".format(a))
    #
    # b = datetime(2019, 4, 1, 12, 0, 1)
    # print(f"{b:%Y-%m-%d %H:%M:%S}")

    c = dict(a="a with test var: {test_var:upper}", b="b", c="c")
    key = "a"
    test_var = StringExtendedFormatOptions("hello, world!")
    # print(f"{c[key]}")

    template = "{c[key]} Test 1, 2, 3"

    # Step 1: Expand dict statements

    # Find all dict statements in the template
    import re

    dict_pattern = re.compile(r"\{(\w+)\[(\w+)\](?::\w+)?\}")
    matches = dict_pattern.findall(template)
    for match in matches:
        dict_name, key_name = match
        key_var = locals()[key_name]
        if dict_name in locals():
            value = locals()[dict_name][key_var]
            template = template.replace(f"{{{dict_name}[{key_name}]}}", value)

    print(template.format(test_var=test_var))

