"""
Tests FW generator
"""
import pytest
import chardet
from app.generator import fw_generator as generator


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
    return 5


@pytest.fixture
def fw_file_op_path(tmp_path):
    # here tmp_path - is a fixture which will provide a temporary directory unique to the test invocation
    return tmp_path / "fwf-op-win1252.txt"


def test_fw_file_encoding_header_no_of_lines(fw_file_op_path, fw_column_width, no_of_lines):
    # creare FWF Generator object
    fwf_generator = generator.FixedWidthFileWriter(
        fw_file_op_path, no_of_lines=no_of_lines, columns=fw_column_width, encoding="windows-1252"
    )

    # call on writer method to generate FWS file at temp location
    fwf_generator.write_file()

    # read generated file and check encoding, no of line, and columns
    raw_data = open(fw_file_op_path, "rb").read()

    result = chardet.detect(raw_data)
    # print ("result : {}".format(result))
    char_enc = result["encoding"]
    # print(char_enc)
    # close(fw_file_op_path)

    # here chardet is not accurate, returns base of win-1252 which is ISO-8859-1
    assert char_enc == "ISO-8859-1"

    # no of lines
    lines_in_file = raw_data.split(b"\r\n")
    assert len(lines_in_file) == no_of_lines + 2  # one header and one blank line at the end

    # get header i.e. first line
    header = lines_in_file[0]

    assert (
        header == b"f1   f2          f3 f4f5           f6     f7        f8           f9                  f10          "
    )
