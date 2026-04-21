"""
Core orchestration module.
Coordinates AI generation, file handling, and Git operations.
"""

import os
from typing import Optional, List
from .code_generator import code_generator
from .file_handler import file_handler
from .git_manager import git_manager
from .logger import logger


class TaskOrchestrator:
    """Orchestrates the complete AI-assisted development workflow."""
    
    def process_task(self, file_path: str, instructions: str, 
                    language: str = "Python", constraints: Optional[str] = None,
                    generate_tests: bool = True) -> bool:
        """
        Process a single development task.
        
        Args:
            file_path: Target file path
            instructions: Code generation instructions
            language: Programming language
            constraints: Optional constraints
            generate_tests: Whether to generate tests
            
        Returns:
            True if successful
        """
        logger.info(f"Processing task for {file_path}")
        
        # Generate code
        code = code_generator.generate_code(instructions, language, constraints)
        if code.startswith("Failed to generate"):
            logger.error(f"Code generation failed: {code}")
            return False
        
        # Check for meaningful changes
        if not file_handler.has_meaningful_changes(file_path, code):
            logger.info("No meaningful changes detected, skipping")
            return True
        
        # Write code file
        if not file_handler.write_code_file(file_path, code, language):
            logger.error("Failed to write code file")
            return False
        
        changed_files = [file_path]
        
        # Generate and write tests
        if generate_tests and language.lower() == "python":
            test_code = code_generator.generate_tests(code, language)
            if not test_code.startswith("Failed to generate"):
                test_file_path = self._get_test_file_path(file_path)
                if file_handler.write_code_file(test_file_path, test_code, language):
                    changed_files.append(test_file_path)
                else:
                    logger.warning("Failed to write test file")
        
        # Commit changes
        if changed_files:
            commit_msg = git_manager.generate_commit_message(changed_files)
            if git_manager.add_files(changed_files) and git_manager.commit_changes(commit_msg):
                git_manager.push_changes()
            else:
                logger.error("Failed to commit changes")
                return False
        
        logger.info(f"Successfully processed task for {file_path}")
        return True
    
    def _get_test_file_path(self, code_file_path: str) -> str:
        """Generate test file path from code file path."""
        base_name = os.path.basename(code_file_path)
        name_without_ext = os.path.splitext(base_name)[0]
        test_name = f"test_{name_without_ext}.py"
        
        # Place in tests directory
        dir_path = os.path.dirname(code_file_path)
        test_dir = os.path.join(dir_path, "..", "tests")
        return os.path.join(test_dir, test_name)
    
    def run_tests(self) -> bool:
        """
        Run test suite.
        
        Returns:
            True if all tests pass
        """
        import subprocess
        try:
            result = subprocess.run(['python', '-m', 'pytest', 'tests/', '-v'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                logger.info("All tests passed")
                return True
            else:
                logger.error(f"Tests failed: {result.stdout}")
                return False
        except FileNotFoundError:
            logger.warning("pytest not found, skipping tests")
            return True
    
    def auto_commit_workflow(self) -> bool:
        """
        Complete auto-commit workflow with testing.
        
        Returns:
            True if successful
        """
        logger.info("Starting auto-commit workflow")
        
        if not git_manager.has_changes():
            logger.info("No changes to commit")
            return True
        
        if not self.run_tests():
            logger.error("Tests failed, aborting commit")
            return False
        
        # Get changed files
        status = git_manager.get_status()
        changed_files = [line.split()[-1] for line in status.split('\n') if line.strip()]
        
        commit_msg = git_manager.generate_commit_message(changed_files)
        
        if git_manager.add_files(changed_files) and git_manager.commit_changes(commit_msg):
            return git_manager.push_changes()
        
        return False


# Global instance
orchestrator = TaskOrchestrator()
