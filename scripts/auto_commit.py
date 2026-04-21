#!/usr/bin/env python3
"""
Auto-commit script for AI-generated changes.
Runs tests, stages changes, commits with meaningful message, and pushes to remote.
Only commits if tests pass and there are meaningful changes.
"""

import sys
import os

# Add project paths
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.orchestrator import orchestrator
from src.logger import logger


def main():
    """Main auto-commit workflow."""
    logger.info("Starting auto-commit process")
    
    success = orchestrator.auto_commit_workflow()
    
    if success:
        logger.info("Auto-commit completed successfully")
        print("Auto-commit completed successfully.")
    else:
        logger.error("Auto-commit failed")
        print("Auto-commit failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
