#!/usr/bin/env python3
"""
Script to update the Ollama model.
Run this periodically to pull the latest version of the model.
"""

import subprocess
import sys
import os

# Add project paths
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.config import Config
from src.logger import logger


def update_model(model: str = None) -> bool:
    """
    Update the specified Ollama model.
    
    Args:
        model: Model name to update, defaults to primary model
        
    Returns:
        True if successful
    """
    model = model or Config.PRIMARY_MODEL
    logger.info(f"Starting update for model: {model}")
    
    try:
        result = subprocess.run(
            ['ollama', 'pull', model], 
            capture_output=True, 
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        if result.returncode == 0:
            logger.info(f"Successfully updated model: {model}")
            print(f"Model {model} updated successfully.")
            return True
        else:
            logger.error(f"Failed to update model {model}: {result.stderr}")
            print(f"Failed to update model: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        logger.error(f"Update timed out for model {model}")
        print("Update timed out.")
        return False
    except FileNotFoundError:
        logger.error("Ollama command not found")
        print("Ollama not installed or not in PATH.")
        return False
    except Exception as e:
        logger.error(f"Error updating model: {e}")
        print(f"Error: {e}")
        return False


def main():
    """Main update function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Update Ollama model")
    parser.add_argument("--model", help="Model name to update")
    args = parser.parse_args()
    
    success = update_model(args.model)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
