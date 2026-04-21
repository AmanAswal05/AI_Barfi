#!/usr/bin/env python3
"""
Main entry point for the AI Personal Assistant project.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from ai.ai_agent import send_prompt

def main():
    # Example usage
    prompt = "Write a simple Python function to calculate factorial."
    response = send_prompt(prompt)
    print("AI Response:")
    print(response)

if __name__ == "__main__":
    main()
