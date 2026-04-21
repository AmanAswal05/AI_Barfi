#!/usr/bin/env python3
"""
Auto-commit script for AI-generated changes.
Stages all changes, commits with a standard message, and pushes to remote.
Only commits if there are actual changes.
"""

import subprocess
import sys

def run_command(command, cwd=None):
    """Run a shell command and return success status."""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def auto_commit():
    """Perform automatic commit and push."""
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
