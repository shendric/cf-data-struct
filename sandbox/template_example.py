# -*- coding: utf-8 -*-
"""

"""

__author__ = "Stefan Hendricks <stefan.hendricks@awi.de>"

from cf_data_struct.template import TemplateEngine

def main() -> None:

    context_attributes = {
        "product": "awi",
        "timeliness": "nrt",
        "version": "v1p0",
        "hemisphere": "nh",
    }

    t = TemplateEngine(context_attributes=context_attributes)
    print(t.render("This is a test template with product: {product}, timeliness: {timeliness}, version: {version}, hemisphere: {hemisphere}."))


if __name__ == "__main__":
    main()
