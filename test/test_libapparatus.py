"""Test functions from the libls package."""
import pytest
import libapparatus


@pytest.fixture(name="logger")
def fixture_logger():
    """Fixture to initialize the logger."""
    lg = libapparatus.get_logger("test_logger", "DEBUG")
    return lg


def test_hash_json():
    """Test the hash_json functions."""
    # Test hash_json
    data = {"key": "value"}
    hash_value = libapparatus.hash_json(data)
    assert isinstance(hash_value, str)
    assert len(hash_value) == 32  # MD5 hash length

    # Test with an empty dictionary
    empty_data = {}
    empty_hash_value = libapparatus.hash_json(empty_data)
    assert isinstance(empty_hash_value, str)
    assert len(empty_hash_value) == 32  # MD5 hash length


def test_logger_basic(logger, caplog):
    """Test basic logging functionality."""
    with caplog.at_level("INFO"):
        logger.info("Test info message")
        assert "Test info message" in caplog.text


def test_logger_warning(logger, caplog):
    """Test warning logging functionality."""
    with caplog.at_level("WARNING"):
        logger.warning("Test warning message")
        assert "Test warning message" in caplog.text


def test_logger_error(logger, caplog):
    """Test error logging functionality."""
    with caplog.at_level("ERROR"):
        logger.error("Test error message")
        assert "Test error message" in caplog.text
