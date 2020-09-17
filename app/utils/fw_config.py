"""
Read json specs and generate python config object

Usage:
    conf = Config(config_file="data/spec.json")
    conf.columns

How to run doc tests?
    > python utils/fw_config.py  -v

>>> conf = Config()
>>> conf.columns
['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10']

>>> conf.offsets
[5, 12, 3, 2, 13, 7, 10, 13, 20, 13]

>>> conf.fixed_width_columns
(('f1', 5), ('f2', 12), ('f3', 3), ('f4', 2), ('f5', 13), ('f6', 7), ('f7', 10), ('f8', 13), ('f9', 20), ('f10', 13))

"""
import json


class Config(object):
    """
    :class:`Config` - Reads ../data/spec.json and prepares python config object

    If not specified returns default encoding value "utf-8"
    """

    def __init__(self, config_file):

        with open(config_file) as f:
            config = json.load(f)

            self.columns = config.get("ColumnNames", [])
            offset = config.get("Offsets", [])
            self.offsets = [int(i) for i in offset] if offset else []
            self.fix_width_encoding = config.get("FixedWidthEncoding", "utf-8")
            self.delimited_encoding = config.get("DelimitedEncoding", "utf-8")
            self.include_header = True if config.get("IncludeHeader", "True") == "True" else False

    @property
    def fixed_width_columns(self):
        """Create a typle of tuples where each tuple represents the
        column name and fixed-width offset i.e (('f1', 5), ('f2',10), ...)
        """
        return tuple(zip(self.columns, self.offsets))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
