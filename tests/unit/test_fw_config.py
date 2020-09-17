"""
Tests FW config
"""
import pytest
from app.utils import fw_config as config


@pytest.fixture
def spec_file_path():
    return "tests/data/spec.json"


@pytest.fixture
def invalid_pec_file_path():
    return "tests/data/spec_doesnot_exist.json"


@pytest.fixture
def spec_incomplete_file_path():
    return "tests/data/spec_incomplete.json"


def test_valid_spec_file(spec_file_path):
    """Test valid spec file"""
    conf = config.Config(spec_file_path)

    assert conf.columns == ["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10"]

    assert conf.offsets == [5, 12, 3, 2, 13, 7, 10, 13, 20, 13]

    assert conf.fixed_width_columns == (
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
    assert conf.fix_width_encoding == "windows-1252"
    assert conf.delimited_encoding == "utf-8"
    assert conf.include_header is True


def test_valid_spec_file(invalid_pec_file_path):
    """
    Check for invalid path
    :param invalid_pec_file_path:
    :return:
    """
    with pytest.raises(FileNotFoundError):
        conf = config.Config(invalid_pec_file_path)


def test_valid_spec_file(spec_incomplete_file_path):
    """Test incomplete spec file"""
    conf = config.Config(spec_incomplete_file_path)

    assert conf.columns == ["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9"]

    assert conf.offsets == [5, 12, 3, 2, 13, 7, 10, 13, 20, 13]

    assert conf.fixed_width_columns == (
        ("f1", 5),
        ("f2", 12),
        ("f3", 3),
        ("f4", 2),
        ("f5", 13),
        ("f6", 7),
        ("f7", 10),
        ("f8", 13),
        ("f9", 20),
    )
    assert conf.fix_width_encoding == "utf-8"  # default encoding "utf-8"
    assert conf.delimited_encoding == "utf-8"
    assert conf.include_header is True
