#!/usr/bin/env python3
"""
Main entry point for the AI Personal Assistant project.
"""

import sys
import os
import subprocess
sys.path.insert(0, os.path.dirname(__file__))

from ai.ai_agent import generate_and_write_code

def run_auto_commit():
    """Run the auto-commit script."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    try:
        result = subprocess.run([sys.executable, "scripts/auto_commit.py"], 
                              capture_output=True, text=True, cwd=project_root)
        print("Auto-commit output:")
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Failed to run auto-commit: {e}")
        return False

def main():
    # Example usage: Generate and write a utility function
    instructions = "Write a Python function to reverse a string."
    constraints = "Use slicing, no built-in reverse methods."
    file_path = "src/utils.py"
    result = generate_and_write_code(instructions, file_path, constraints=constraints)
    print(result)
    
    # Automatically commit changes
    if "successfully written" in result:
        run_auto_commit()
    
    # Display the updated file
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            print(f"\nUpdated code in {file_path}:")
            print(f.read())

if __name__ == "__main__":
    main()
