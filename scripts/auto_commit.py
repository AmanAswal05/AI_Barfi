#!/usr/bin/env python3
"""
Auto-commit script for AI-generated changes.
Runs tests, stages all changes, commits with a standard message, and pushes to remote.
Only commits if tests pass and there are changes.
"""

import subprocess
import sys
import os

def run_command(command, cwd=None):
    """Run a shell command and return success status."""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def run_tests():
    """Run pytest and return success status."""
    print("Running tests...")
    success, stdout, stderr = run_command("python -m pytest tests/ -v")
    if success:
        print("All tests passed.")
        return True
    else:
        print("Tests failed!")
        print("STDOUT:", stdout)
        print("STDERR:", stderr)
        return False

def auto_commit():
    """Perform automatic commit and push."""
    # Run tests first
    if not run_tests():
        print("Aborting commit due to test failures.")
        return False
    
    # Check for changes
    success, stdout, stderr = run_command("git status --porcelain")
    if not success:
        print(f"Error checking git status: {stderr}")
        return False
    
    if not stdout.strip():
        print("No changes to commit.")
        return True
    
    # Stage changes
    success, stdout, stderr = run_command("git add .")
    if not success:
        print(f"Error staging changes: {stderr}")
        return False
    
    # Commit
    commit_message = "AI-generated update"
    success, stdout, stderr = run_command(f'git commit -m "{commit_message}"')
    if not success:
        print(f"Error committing changes: {stderr}")
        return False
    
    print(f"Committed changes: {commit_message}")
    
    # Push
    success, stdout, stderr = run_command("git push")
    if not success:
        print(f"Error pushing changes: {stderr}")
        return False
    
    print("Changes pushed to remote repository.")
    return True

if __name__ == "__main__":
    if auto_commit():
        print("Auto-commit completed successfully.")
        sys.exit(0)
    else:
        print("Auto-commit failed.")
        sys.exit(1)
