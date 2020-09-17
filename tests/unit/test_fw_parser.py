"""
Tests FW generator
"""
import pytest
import csv
from app.parser import fw_parser as parser


@pytest.fixture
def fw_column_width():
    return (
        ("f1", 5),
        ("f2", 12),
        ("f3", 3),
        ("f4", 2),
        ("f5", 13),
        ("f6", 7),
        ("f7", 10),
        ("f8", 13),
        ("f9", 20),
        ("f10", 13),
    )


@pytest.fixture
def no_of_lines():
    return 100


@pytest.fixture
def fw_file_ip_path():
    return "tests/data/fwf-win1252.txt"


@pytest.fixture
def csv_file_op_path(tmp_path):
    # here tmp_path - is a fixture which will provide a temporary directory unique to the test invocation
    return tmp_path / "csv-op-utf-8.csv"


@pytest.fixture
def valid_parser_object(fw_file_ip_path, csv_file_op_path, fw_column_width):
    return parser.FWFParser(
        fw_file_ip_path, csv_file_op_path, columns=fw_column_width, fwf_encoding="windows-1252", csv_encoding="utf-8"
    )


def test_fw_parser_header(valid_parser_object, fw_column_width):

    # create parser object
    fwf_parser = valid_parser_object

    # get header
    header = valid_parser_object._get_header()

    assert header == list(dict(fw_column_width).keys())


def test_fw_parser_no_of_lines(valid_parser_object, no_of_lines):

    # create parser object
    fwf_parser = valid_parser_object

    # checking the FWF file name
    assert fwf_parser.fwf_file == "tests/data/fwf-win1252.txt"

    # fwf_parser.content -> actually yields line by line, so total line count should be 102
    file_parsed_dict = list(fwf_parser.content)
    print(len(file_parsed_dict))
    assert len(file_parsed_dict) == no_of_lines, "No of lines must be equal to 100"


def test_fw_parser_header(valid_parser_object, fw_column_width):
    # create parser object
    fwf_parser = valid_parser_object

    # fwf_parser.content -> actually yields line by line
    parsed_dict = next(fwf_parser.content)

    # print(list(parsed_dict.keys()))
    # print(list(dict(fw_column_width).keys()))

    assert list(parsed_dict.keys()) == list(dict(fw_column_width).keys()), "Header didn't match"


@pytest.mark.parametrize("write_header", [True, False])
def test_fw_parser_csv_dump(write_header, valid_parser_object, csv_file_op_path, no_of_lines):
    # generate CSV @ csv_file_op_path
    valid_parser_object.dump_csv(write_header=write_header)

    parser_headers = valid_parser_object._get_header()

    # assuming utf-8 encoding
    with open(csv_file_op_path, "r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=parser_headers)

        # checking headers in CSV
        csv_rows = list(reader)

        header = csv_rows[0]
        print(header)

        if write_header:
            # headers row matches only if write_header=True
            assert list(header.values()) == parser_headers
        else:
            # headers row doesn't match if write_header=False
            assert list(header.values()) != parser_headers

        # checking no of line in CSV
        if write_header:
            # write_header=True have extra header row
            assert len(csv_rows) == no_of_lines + 1
        else:
            assert len(csv_rows) == no_of_lines
