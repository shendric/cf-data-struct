# -*- coding: utf-8 -*-

"""
The datastruct models contains the data structures
"""

__author__ = "Stefan Hendricks <stefan.hendricks@awi.de>"
__all__ = ["datamodels", "datastruct", "TemplateEngine", "TrajectoryCFStruct", "GridCFStruct", "CFVariable"]

from cf_data_struct.datastruct import (CFVariable, GridCFStruct, TrajectoryCFStruct)
from cf_data_struct.template import TemplateEngine