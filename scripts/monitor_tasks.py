#!/usr/bin/env python3
"""
Monitor tasks.txt for changes and automatically process AI code generation tasks.
Format in tasks.txt: file_path | instructions | constraints
Example: src/utils.py | Write a function to sort a list | Use built-in sorted
"""

import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Add project paths
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ai.ai_agent import generate_and_write_code

class TaskHandler(FileSystemEventHandler):
    def __init__(self, tasks_file):
        self.tasks_file = tasks_file
        self.last_processed = set()
    
    def on_modified(self, event):
        if event.src_path == self.tasks_file:
            self.process_tasks()
    
    def process_tasks(self):
        """Read and process tasks from the file."""
        if not os.path.exists(self.tasks_file):
            return
        
        with open(self.tasks_file, 'r') as f:
            lines = f.readlines()
        
        new_tasks = []
        for line in lines:
            line = line.strip()
            if line and line not in self.last_processed:
                new_tasks.append(line)
        
        if not new_tasks:
            return
        
        print(f"Processing {len(new_tasks)} new task(s)...")
        
        for task in new_tasks:
            try:
                parts = [p.strip() for p in task.split('|')]
                if len(parts) < 2:
                    print(f"Invalid task format: {task}")
                    continue
                
                file_path = parts[0]
                instructions = parts[1]
                constraints = parts[2] if len(parts) > 2 else None
                
                print(f"Generating code for {file_path}...")
                result = generate_and_write_code(instructions, file_path, constraints=constraints)
                print(result)
                
                self.last_processed.add(task)
            
            except Exception as e:
                print(f"Error processing task '{task}': {e}")
        
        # Clear processed tasks from file
        with open(self.tasks_file, 'w') as f:
            remaining = [line for line in lines if line.strip() not in self.last_processed]
            f.writelines(remaining)
        
        # Auto-commit changes
        if new_tasks:
            self.run_auto_commit()
    
    def run_auto_commit(self):
        """Run the auto-commit script."""
        try:
            result = subprocess.run([sys.executable, "scripts/auto_commit.py"], 
                                  capture_output=True, text=True)
            print("Auto-commit output:")
            print(result.stdout)
            if result.stderr:
                print("Errors:", result.stderr)
        except Exception as e:
            print(f"Failed to run auto-commit: {e}")

def main():
    tasks_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tasks.txt")
    
    event_handler = TaskHandler(tasks_file)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(tasks_file), recursive=False)
    
    print(f"Monitoring {tasks_file} for changes. Add tasks in format: file_path | instructions | constraints")
    print("Press Ctrl+C to stop.")
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopped monitoring.")
    observer.join()

if __name__ == "__main__":
    main()
