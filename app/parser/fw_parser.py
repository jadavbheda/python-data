"""FWF parser
"""

import sys
import logging as log
import csv

from utils import fw_config as config

# TODO - move logger in single file
ROOT = log.getLogger()
ROOT.setLevel(log.INFO)

if not ROOT.hasHandlers():
    HANDLER = log.StreamHandler(sys.stdout)
    HANDLER.setLevel(log.INFO)
    FORMATTER = log.Formatter('%(asctime)s:%(name)s:%(levelname)s: %(message)s')
    HANDLER.setFormatter(FORMATTER)
    ROOT.addHandler(HANDLER)


class FWFParser(object):
    """
    Note* - Code is not python2 compatible.

    In python3: string literals are unicode by default. Also IO supports encodings.
    So we don't need to explicitly manage encodings.

    However in python2 string literals are ASCII. So if using python-2 below thing had to be managed manually.

    FWF is cp1252 encoded, while result CSV needs to be utf-8

    Unicode sandwitch:
        str (unicode) -> encode -> bytes
        bytes -> decode -> str (unicode)

    That mean once reading bytes from FWF we need decode('cp1252')

    reference - http://xahlee.info/python/charset_encoding.html
    """
    def __init__(self, fwf_file, csv_file, columns, fwf_encoding='cp1252', csv_encoding='utf-8'):
        """
        FWFParser class parses FWF and provids method to convert it to CSV

        :param fw_file: Input FWF file
        :param csv_file: output CSV file
        :param columns: is a list of tuples that represent the column and offset definitions.  For example::
                [
                    ('f1', 3),
                    ('f2', 12),
                    ('f3', 3),
                    ...
                ]
        :param fwf_encoding: FWF file encoding
        :param csv_encoding: CSV file encoding
        """
        self.fwf_file = fwf_file
        self.csv_file = csv_file
        self.offsets = columns
        self.fwf_encoding = 'cp1252' if fwf_encoding == 'windows-1252' else fwf_encoding
        self.csv_encoding = 'cp1252' if csv_encoding == 'windows-1252' else csv_encoding

        # calling internal parsing method
        self.content = self._parser()

    def _get_header(self):
        """
        generated FWF header
        :return:
        """
        header = [col_name for col_name, width in self.offsets]

        return header

    def _parser(self):
        """
        FWF file parser, yields {'f1': value, 'f2': value} for every line in the file
        :return:
        """
        with open(self.fwf_file, encoding=self.fwf_encoding) as _fh:
            for line_number, line in enumerate(_fh):
                if line_number == 0:
                    # ignore header row
                    continue

                # TODO - assuming line ending in \r\n but there has to be more generic way of doing it
                raw_line = line.rstrip('\r\n')
                yield self._parse_line(raw_line)

    def _parse_line(self, line):
        """Split list if characters defined by *line* into field values delimited by
        the column and offset definitions within *offsets*.

        """
        parsed_line = {}
        start_index = 0
        for column, offset in self.offsets:
            # TODO- initial thought to use `struct` because its faster, but seems like it can't operate on non-ascii
            # so for now not wasting time and using slicing
            parsed_line.update({column: line[start_index:start_index+offset].rstrip()})
            start_index += offset

        return parsed_line

    def dump_csv(self, write_header=True):
        """
        dump into CSV
        :param write_header: if true
        :return:
        """
        log.info('Writing to CSV file: {}'.format(self.csv_file))
        log.info('Headers : {}'.format(self._get_header()))
        counter = 0
        with open(self.csv_file, 'w', newline='', encoding=self.csv_encoding) as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self._get_header())
            if write_header:
                writer.writeheader()

            for line in self.content:
                writer.writerow(line)
                counter += 1

        log.info('CSV records written to "%s": %d', csv_file, counter)

        return counter
