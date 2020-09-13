#!/usr/bin/env python
import os

from utils import fw_config as config
from parser import fw_parser as parser
from generator import fw_generator as generator

# globals
# All file paths config below (could have read it from the config file

# problem-1 globals
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__)) # `app` is our project root
FW_SPEC = os.path.join(PROJECT_ROOT, 'data/spec.json')
FW_FILE = os.path.join(PROJECT_ROOT, 'data/fwf.txt')
CSV_FILE = os.path.join(PROJECT_ROOT, 'data/converted.csv')

#problem-2 globals
# TBD


def problem_1_fix_width_to_csv():
    """
    Wrapper to convert FW to CSV. Does following.
        - Generate fix width file with given spec in spec.json
        - Parse FW file,
        - and generate CSV

    Note*
        - Haven't spent any efforts in making it configurable, or reading input from the command line.
        - I.e. reading and writing into a fix path, for now

    :return:
    """

    # get fix width spec in conf python object
    conf = config.Config(FW_SPEC)

    print("Generating Fix width file (windows-1252) .... [{}]".format(FW_FILE))
    fwf_generator = generator.FixedWidthFileWriter(FW_FILE,
                                                   columns=conf.fixed_width_columns,
                                                   encoding=conf.fix_width_encoding
                                                   )
    fwf_generator.write_file()

    print("Parsing Fix width file....[{}]".format(FW_FILE))
    fwf_parser = parser.FWFParser(FW_FILE,
                                  CSV_FILE,
                                  columns=conf.fixed_width_columns,
                                  fwf_encoding=conf.fix_width_encoding,
                                  csv_encoding=conf.delimited_encoding
                                  )

    print("Generating CSV file...[{}]".format(CSV_FILE))
    fwf_parser.dump_csv(write_header=conf.include_header)


def problem_2_data_processing():
    """
    Wrapper to annonymise input data - planning to use Faker
    :return:
    """
    # TBD -
    pass


def main():
    """
    Script entry point.
    """
    problem_1_fix_width_to_csv()


if __name__ == '__main__':
    main()
