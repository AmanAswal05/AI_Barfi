"""
File handling module.
Provides safe file operations with validation and backups.
"""

import os
import hashlib
from typing import Optional
from .config import Config
from .logger import logger


class FileHandler:
    """Handles file operations safely."""
    
    def _validate_code(self, code: str, language: str) -> bool:
        """Validate code syntax."""
        if language.lower() == "python":
            try:
                compile(code, '<string>', 'exec')
                return True
            except SyntaxError as e:
                logger.error(f"Syntax error in generated code: {e}")
                return False
        return True  # Assume valid for other languages
    
    def _create_backup(self, file_path: str) -> Optional[str]:
        """Create backup of existing file."""
        if not os.path.exists(file_path):
            return None
        
        backup_path = file_path + Config.BACKUP_SUFFIX
        try:
            os.rename(file_path, backup_path)
            logger.info(f"Created backup: {backup_path}")
            return backup_path
        except OSError as e:
            logger.error(f"Failed to create backup: {e}")
            return None
    
    def _get_file_hash(self, file_path: str) -> Optional[str]:
        """Get SHA256 hash of file content."""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except OSError:
            return None
    
    def write_code_file(self, file_path: str, code: str, language: str = "Python") -> bool:
        """
        Write code to file safely.
        
        Args:
            file_path: Path to write to
            code: Code content
            language: Programming language
            
        Returns:
            True if successful, False otherwise
        """
        if not self._validate_code(code, language):
            logger.error("Code validation failed, not writing file")
            return False
        
        # Create directory if needed
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Create backup
        backup_path = self._create_backup(file_path)
        
        try:
            with open(file_path, 'w') as f:
                f.write(code)
            logger.info(f"Successfully wrote code to {file_path}")
            
            # Verify write
            if self._get_file_hash(file_path) != hashlib.sha256(code.encode()).hexdigest():
                logger.error("File write verification failed")
                # Restore backup if exists
                if backup_path:
                    os.rename(backup_path, file_path)
                return False
            
            return True
        except OSError as e:
            logger.error(f"Failed to write file {file_path}: {e}")
            return False
    
    def has_meaningful_changes(self, file_path: str, new_content: str) -> bool:
        """
        Check if new content represents meaningful changes.
        
        Args:
            file_path: File to check
            new_content: New content
            
        Returns:
            True if changes are meaningful
        """
        if not os.path.exists(file_path):
            return True
        
        try:
            with open(file_path, 'r') as f:
                old_content = f.read()
            
            # Simple check: different content and not just whitespace/comments
            if old_content.strip() != new_content.strip():
                # Check if it's more than just formatting
                old_lines = [line.strip() for line in old_content.split('\n') if line.strip() and not line.strip().startswith('#')]
                new_lines = [line.strip() for line in new_content.split('\n') if line.strip() and not line.strip().startswith('#')]
                return old_lines != new_lines
            
            return False
        except OSError:
            return True


# Global instance
file_handler = FileHandler()
