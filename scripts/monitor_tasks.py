#!/usr/bin/env python3
"""
Monitor tasks.txt for changes and automatically process AI code generation tasks.
Format in tasks.txt: file_path | instructions | constraints
Example: src/utils.py | Write a function to sort a list | Use built-in sorted
"""

import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Add project paths
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.orchestrator import orchestrator
from src.utils import load_tasks_from_file, parse_task_line
from src.logger import logger


class TaskHandler(FileSystemEventHandler):
    """Handles file system events for task processing."""
    
    def __init__(self, tasks_file: str):
        self.tasks_file = tasks_file
        self.last_processed = set()
    
    def on_modified(self, event):
        """Handle file modification events."""
        if event.src_path == self.tasks_file:
            self.process_tasks()
    
    def process_tasks(self):
        """Read and process new tasks from the file."""
        tasks = load_tasks_from_file(self.tasks_file)
        
        new_tasks = []
        for task_tuple in tasks:
            task_line = f"{task_tuple[0]} | {task_tuple[1]} | {task_tuple[2]}"
            if task_line not in self.last_processed:
                new_tasks.append(task_tuple)
        
        if not new_tasks:
            return
        
        logger.info(f"Processing {len(new_tasks)} new task(s)...")
        
        for file_path, instructions, constraints in new_tasks:
            try:
                success = orchestrator.process_task(
                    file_path=file_path,
                    instructions=instructions,
                    constraints=constraints or None
                )
                if success:
                    task_line = f"{file_path} | {instructions} | {constraints}"
                    self.last_processed.add(task_line)
                    logger.info(f"Successfully processed task for {file_path}")
                else:
                    logger.error(f"Failed to process task for {file_path}")
            except Exception as e:
                logger.error(f"Error processing task {file_path}: {e}")


def main():
    """Main monitoring function."""
    tasks_file = "tasks.txt"
    
    if not os.path.exists(tasks_file):
        logger.warning(f"Tasks file {tasks_file} not found, creating empty file")
        with open(tasks_file, 'w') as f:
            f.write("# Add tasks in format: file_path | instructions | constraints\n")
    
    event_handler = TaskHandler(tasks_file)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    
    logger.info(f"Monitoring {tasks_file} for changes. Add tasks in format: file_path | instructions | constraints")
    logger.info("Press Ctrl+C to stop.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("Monitoring stopped")
    
    observer.join()


if __name__ == "__main__":
    main()
