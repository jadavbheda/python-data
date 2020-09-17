"""
Fix width file generator
"""
import string
import random
from faker import Faker


class FixedWidthFileWriter(object):
    def __init__(self, op_file, columns, no_of_lines=100, encoding="cp1252"):
        """Generates FWF by default in cp1252 encoding

        :param op_file: O/p file to be generated
        :param columns: is a list of tuples that represent the column and offset definitions.  For example::
                [
                    ('f1', 3),
                    ('f2', 12),
                    ('f3', 3),
                    ...
                ]
        :param no_of_lines: no of lines to be generated
        :param encoding: o/p file encoding default is cp1252
        """
        self.op_file = op_file
        self.columns = columns
        self.no_of_lines = no_of_lines
        self.encoding = "cp1252" if encoding == "windows-1252" else encoding

    def get_header(self):
        """
        generated FWF header
        :return:
        """
        header = "".join([col_name.ljust(width) for col_name, width in self.columns])

        return header

    def write_file(self):
        """
        Generate FWF
        :return:
        """
        # using Faker to generate realistic data
        locale = ["de_DE", "fr_FR", "en_AU"]
        fake = Faker(locale)

        try:
            # python3 default is unicode - utf-8
            # encoding format to use: cp1252 - windows-1252 (Western Europe)
            with open(self.op_file, "w", encoding=self.encoding) as f:
                # write header first
                header = self.get_header()
                f.write(header)
                # TODO- I think windows-1252 uses windows line ending. Not sure if there is better way to do it
                f.write("\r\n")

                # write no of lines in file
                for line in range(self.no_of_lines):
                    line_text = ""

                    # line must contain all columns of given length
                    # using Faker to generate locale specific strings
                    # but faker can't generate strings less than 5 chars, in that case using random.choices
                    for col_name, width in self.columns:
                        if width > 5:
                            col_value = fake.text(width - 1)
                        else:
                            col_value = "".join(random.choices(string.ascii_lowercase, k=width - 1))

                        line_text += col_value.ljust(width)
                    f.write(line_text)
                    f.write("\r\n")

        except OSError as e:
            # 'File not found' error
            print("Invalid O/P FWF file path {}".format(self.op_file))
            raise e
