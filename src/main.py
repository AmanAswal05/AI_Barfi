#!/usr/bin/env python3
"""
Main entry point for the AI Assistant.
Demonstrates basic usage and provides CLI interface.
"""

import sys
import argparse
from src.orchestrator import orchestrator
from src.logger import logger


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="AI-Powered Code Generation Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/main.py --file src/utils.py --instructions "Write a factorial function"
  python src/main.py --task-file tasks.txt
  python src/main.py --dashboard
        """
    )
    
    parser.add_argument(
        "--file", "-f",
        help="Target file path"
    )
    parser.add_argument(
        "--instructions", "-i",
        help="Code generation instructions"
    )
    parser.add_argument(
        "--constraints", "-c",
        help="Optional constraints"
    )
    parser.add_argument(
        "--task-file",
        help="Process tasks from file"
    )
    parser.add_argument(
        "--dashboard", 
        action="store_true",
        help="Start web dashboard"
    )
    parser.add_argument(
        "--auto-commit",
        action="store_true", 
        help="Run auto-commit workflow"
    )
    
    args = parser.parse_args()
    
    if args.dashboard:
        logger.info("Starting dashboard...")
        from src.dashboard import app
        app.run(debug=True, host='0.0.0.0', port=5000)
        return
    
    if args.auto_commit:
        logger.info("Running auto-commit workflow...")
        success = orchestrator.auto_commit_workflow()
        print("Auto-commit successful" if success else "Auto-commit failed")
        sys.exit(0 if success else 1)
    
    if args.task_file:
        logger.info(f"Processing tasks from {args.task_file}")
        from src.utils import load_tasks_from_file
        tasks = load_tasks_from_file(args.task_file)
        for file_path, instructions, constraints in tasks:
            success = orchestrator.process_task(
                file_path=file_path,
                instructions=instructions,
                constraints=constraints or None
            )
            if not success:
                logger.error(f"Failed to process task for {file_path}")
                sys.exit(1)
        print("All tasks processed successfully")
        return
    
    if args.file and args.instructions:
        logger.info(f"Processing single task: {args.file}")
        success = orchestrator.process_task(
            file_path=args.file,
            instructions=args.instructions,
            constraints=args.constraints
        )
        if success:
            print(f"Code generated successfully for {args.file}")
        else:
            print(f"Failed to generate code for {args.file}")
            sys.exit(1)
        return
    
    parser.print_help()


if __name__ == "__main__":
    main()
