"""
Tests for utility functions.
"""

import pytest
import tempfile
import os
from src.utils import parse_task_line, load_tasks_from_file, save_history


def test_parse_task_line():
    """Test task line parsing."""
    # Full format
    file_path, instructions, constraints = parse_task_line("src/utils.py | Write function | Use built-ins")
    assert file_path == "src/utils.py"
    assert instructions == "Write function"
    assert constraints == "Use built-ins"
    
    # Without constraints
    file_path, instructions, constraints = parse_task_line("src/utils.py | Write function")
    assert file_path == "src/utils.py"
    assert instructions == "Write function"
    assert constraints == ""
    
    # Invalid format
    with pytest.raises(ValueError):
        parse_task_line("invalid")


def test_load_tasks_from_file():
    """Test loading tasks from file."""
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("# Comment\n")
        f.write("src/utils.py | Write function | Use built-ins\n")
        f.write("src/main.py | Main function\n")
        temp_file = f.name
    
    try:
        tasks = load_tasks_from_file(temp_file)
        assert len(tasks) == 2
        assert tasks[0] == ("src/utils.py", "Write function", "Use built-ins")
        assert tasks[1] == ("src/main.py", "Main function", "")
    finally:
        os.unlink(temp_file)


def test_save_history():
    """Test saving generation history."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        temp_file = f.name
    
    try:
        save_history("Test instructions", "def test(): pass", "test.py")
        
        with open('ai_history.txt', 'r') as f:
            content = f.read()
            assert "Test instructions" in content
            assert "test.py" in content
            assert "def test(): pass" in content
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)
        if os.path.exists('ai_history.txt'):
            os.unlink('ai_history.txt')
