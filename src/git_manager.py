"""
Git management module.
Handles version control operations with meaningful commits.
"""

import subprocess
import os
from typing import List, Optional
from .config import Config
from .logger import logger


class GitManager:
    """Manages Git operations."""
    
    def _run_git_command(self, command: List[str], cwd: Optional[str] = None) -> tuple[bool, str]:
        """Run a git command and return success status and output."""
        try:
            result = subprocess.run(
                ['git'] + command,
                capture_output=True,
                text=True,
                cwd=cwd,
                check=True
            )
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed: {' '.join(command)} - {e.stderr}")
            return False, e.stderr.strip()
    
    def get_status(self) -> str:
        """Get current git status."""
        success, output = self._run_git_command(['status', '--porcelain'])
        return output if success else ""
    
    def has_changes(self) -> bool:
        """Check if there are uncommitted changes."""
        status = self.get_status()
        return bool(status.strip())
    
    def add_files(self, files: List[str]) -> bool:
        """Add files to staging area."""
        success, _ = self._run_git_command(['add'] + files)
        if success:
            logger.info(f"Added files to git: {files}")
        return success
    
    def commit_changes(self, message: str) -> bool:
        """
        Commit changes with meaningful message.
        
        Args:
            message: Commit message
            
        Returns:
            True if committed successfully
        """
        if not self.has_changes():
            logger.info("No changes to commit")
            return True
        
        success, _ = self._run_git_command(['commit', '-m', message])
        if success:
            logger.info(f"Committed changes: {message}")
        return success
    
    def push_changes(self) -> bool:
        """Push changes to remote."""
        success, _ = self._run_git_command(['push', Config.GIT_REMOTE, Config.GIT_BRANCH])
        if success:
            logger.info("Pushed changes to remote")
        return success
    
    def generate_commit_message(self, changed_files: List[str]) -> str:
        """
        Generate context-aware commit message.
        
        Args:
            changed_files: List of changed files
            
        Returns:
            Commit message
        """
        if not changed_files:
            return "AI-generated updates"
        
        # Categorize files
        code_files = [f for f in changed_files if f.endswith(('.py', '.js', '.ts', '.java'))]
        test_files = [f for f in changed_files if 'test' in f.lower()]
        config_files = [f for f in changed_files if f.endswith(('.json', '.yaml', '.yml', '.toml'))]
        
        parts = []
        if code_files:
            parts.append(f"Add/update {len(code_files)} code file(s)")
        if test_files:
            parts.append(f"Add/update {len(test_files)} test file(s)")
        if config_files:
            parts.append(f"Update {len(config_files)} config file(s)")
        
        if not parts:
            parts.append("Update files")
        
        return f"AI-generated: {', '.join(parts)}"


# Global instance
git_manager = GitManager()
