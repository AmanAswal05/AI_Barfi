"""
Code generation module.
Handles code generation, cleaning, and formatting.
"""

import subprocess
import tempfile
from typing import Optional
from .ai_client import ai_client
from .logger import logger


class CodeGenerator:
    """Handles code generation and processing."""
    
    def _clean_code_output(self, code: str) -> str:
        """Clean AI-generated code by removing markdown."""
        code = code.strip()
        if code.startswith('```') and '```' in code[3:]:
            start = code.find('```') + 3
            end = code.rfind('```')
            if start < end:
                code = code[start:end].strip()
                # Remove language identifier
                if '\n' in code:
                    first_line, rest = code.split('\n', 1)
                    if not first_line or first_line.lower() in ['python', 'py']:
                        code = rest
        code = code.replace('```', '').strip()
        return code
    
    def _format_code(self, code: str, language: str) -> str:
        """Format code using appropriate tools."""
        if language.lower() == "python":
            try:
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                    f.write(code)
                    temp_file = f.name
                subprocess.run(['black', temp_file], capture_output=True, check=True)
                with open(temp_file, 'r') as f:
                    code = f.read()
                import os
                os.unlink(temp_file)
                logger.debug("Code formatted with black")
            except (subprocess.CalledProcessError, FileNotFoundError):
                logger.warning("Black formatting failed, using original code")
        return code
    
    def generate_code(self, instructions: str, language: str = "Python", constraints: Optional[str] = None) -> str:
        """
        Generate code based on instructions.
        
        Args:
            instructions: Description of what code to generate
            language: Programming language
            constraints: Optional constraints
            
        Returns:
            Generated and cleaned code
        """
        context = f"You are an expert {language} programmer. Generate high-quality {language} code."
        prompt = f"{context}\n\nInstructions: {instructions}\n\nRespond ONLY with raw {language} code. No markdown, explanations, or extra text."
        if constraints:
            prompt += f"\nConstraints: {constraints}"
        
        raw_code = ai_client.generate_response(prompt)
        if raw_code.startswith("Failed to generate"):
            return raw_code
        
        cleaned_code = self._clean_code_output(raw_code)
        formatted_code = self._format_code(cleaned_code, language)
        
        logger.info(f"Generated {language} code for: {instructions[:30]}...")
        return formatted_code
    
    def generate_tests(self, code: str, language: str = "Python") -> str:
        """
        Generate tests for given code.
        
        Args:
            code: The code to test
            language: Programming language
            
        Returns:
            Generated test code
        """
        if language.lower() != "python":
            return ""
        
        prompt = f"Write comprehensive pytest tests for this Python code:\n\n{code}\n\nRespond ONLY with raw Python test code. Start with imports."
        
        raw_tests = ai_client.generate_response(prompt)
        if raw_tests.startswith("Failed to generate"):
            return raw_tests
        
        cleaned_tests = self._clean_code_output(raw_tests)
        formatted_tests = self._format_code(cleaned_tests, language)
        
        logger.info("Generated test code")
        return formatted_tests


# Global instance
code_generator = CodeGenerator()
