"""
Read config and generate python config object
"""
import json


class Config:
    """
    :class:`Config` - Reads ../data/spec.json and prepares python config object
    """
    def __init__(self, config_file='data/spec.json'):
        with open(config_file) as f:
            #TODO - assuming file exists and in the valid format
            config = json.load(f)

            self.columns = config.get('ColumnNames', [])
            offset = config.get('Offsets', [])
            self.offsets = [int(i) for i in offset] if offset else []
            self.fix_width_encoding = config.get('FixedWidthEncoding')
            self.delimited_encoding = config.get('DelimitedEncoding')
            self.include_header = config.get('IncludeHeader')

    @property
    def fixed_width_columns(self):
        """Create a typle of tuples where each tuple represents the
        column name and fixed-width offset i.e (('f1', 5), ('f2',10), ...)
        """
        return tuple(zip(self.columns, self.offsets))