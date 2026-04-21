#!/usr/bin/env python3
"""
Main entry point for the AI Personal Assistant project.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from ai.ai_agent import generate_and_write_code

def main():
    # Example usage: Generate and write a utility function
    instructions = "Write a Python function to calculate the Fibonacci sequence up to n terms."
    constraints = "Use an iterative approach, return a list of integers."
    file_path = "src/utils.py"
    result = generate_and_write_code(instructions, file_path, constraints=constraints)
    print(result)
    
    # Optionally, read and display the generated file
    if "successfully written" in result:
        with open(file_path, 'r') as f:
            print("\nGenerated code in utils.py:")
            print(f.read())

if __name__ == "__main__":
    main()
