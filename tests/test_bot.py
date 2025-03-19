import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Ensure project root is in Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import is_abusive, update_encouragements, delete_encouragement, get_quote

try:
    from replit import db
except ImportError:
    db = {}

@pytest.mark.parametrize("message, expected", [
    ("This is a normal message", False),
    ("You are a bitch!", True),
    ("Go to hell, mother fucker!", True),
    ("Have a nice day!", False)
])
def test_is_abusive(message, expected):
    """Test if abusive words are correctly detected."""
    assert is_abusive(message) == expected

@patch("replit.db", create=True)
def test_update_encouragements(mock_db):
    """Test adding an encouragement message."""
    test_message = "Keep going, you're awesome!"

    # Mocking the database correctly
    mock_db.keys.return_value = ["encouragements"]
    mock_db.__contains__.side_effect = lambda key: key in ["encouragements"]
    mock_db.__getitem__.side_effect = lambda key: ["Test message"] if key == "encouragements" else []
    mock_db.__setitem__.side_effect = lambda key, value: mock_db.update({key: value})

    update_encouragements(test_message)

    assert test_message in mock_db["encouragements"]

@patch("replit.db", create=True)
def test_delete_encouragement(mock_db):
    """Test deleting an encouragement message."""
    # Mocking the database correctly
    mock_db.keys.return_value = ["encouragements"]
    mock_db.__getitem__.side_effect = lambda key: ["Test message"] if key == "encouragements" else []
    mock_db.__setitem__.side_effect = lambda key, value: mock_db.update({key: value})

    result = delete_encouragement(0)

    assert result == "Encouragement deleted."
    assert len(mock_db["encouragements"]) == 0  # List should be empty now

@patch("requests.get")
def test_get_quote(mock_get):
    """Test fetching an inspirational quote."""
    mock_get.return_value.json.return_value = [{"q": "Test Quote", "a": "Author"}]

    quote = get_quote()

    assert "Test Quote" in quote  # Ensures quote is returned correctly
