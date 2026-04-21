"""
Utility functions for the AI assistant.
"""

import os
from typing import List, Tuple


def parse_task_line(line: str) -> Tuple[str, str, str]:
    """
    Parse a task line in format: file_path | instructions | constraints
    
    Args:
        line: Task line to parse
        
    Returns:
        Tuple of (file_path, instructions, constraints)
    """
    parts = line.split('|', 2)
    if len(parts) == 3:
        return parts[0].strip(), parts[1].strip(), parts[2].strip()
    elif len(parts) == 2:
        return parts[0].strip(), parts[1].strip(), ""
    else:
        raise ValueError(f"Invalid task format: {line}")


def load_tasks_from_file(file_path: str) -> List[Tuple[str, str, str]]:
    """
    Load tasks from a file.
    
    Args:
        file_path: Path to task file
        
    Returns:
        List of (file_path, instructions, constraints) tuples
    """
    tasks = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    try:
                        tasks.append(parse_task_line(line))
                    except ValueError as e:
                        print(f"Warning: {e}")
    return tasks


def save_history(instructions: str, code: str, file_path: str) -> None:
    """
    Save generation history.
    
    Args:
        instructions: Generation instructions
        code: Generated code
        file_path: Target file path
    """
    with open('ai_history.txt', 'a') as f:
        f.write(f"Instructions: {instructions}\n")
        f.write(f"File: {file_path}\n")
        f.write(f"Code:\n{code}\n")
        f.write("---\n")
