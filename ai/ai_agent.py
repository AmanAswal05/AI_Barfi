import requests
import os
import subprocess
import tempfile
import logging

# Set up logging
logging.basicConfig(filename='ai_actions.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def send_prompt(prompt, model="codellama"):
    """
    Send a prompt to the local Ollama AI model and return the response.
    
    Args:
        prompt (str): The prompt to send to the AI.
        model (str): The model name, default is 'codellama'.
    
    Returns:
        str: The AI's response.
    """
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        logging.info(f"Sending prompt to {model}: {prompt[:100]}...")
        response = requests.post(url, json=data)
        response.raise_for_status()
        result = response.json()["response"]
        logging.info(f"Received response from {model}, length: {len(result)}")
        return result
    except requests.exceptions.RequestException as e:
        logging.error(f"Error communicating with Ollama: {e}")
        return f"Error communicating with Ollama: {e}"

def clean_code_output(code):
    """Clean AI-generated code by removing markdown and extracting code blocks."""
    code = code.strip()
    if code.startswith('```') and '```' in code[3:]:
        # Extract content between first and last ```
        start = code.find('```') + 3
        end = code.rfind('```')
        if start < end:
            code = code[start:end].strip()
            # Remove language identifier if present
            if '\n' in code:
                first_line, rest = code.split('\n', 1)
                if not first_line or first_line.lower() in ['python', 'py']:
                    code = rest
    # Remove any remaining ```
    code = code.replace('```', '').strip()
    return code

def generate_code(instructions, language="Python", constraints=None):
    """
    Generate code using the local AI based on structured instructions.
    
    Args:
        instructions (str): The coding task description.
        language (str): The programming language, default is 'Python'.
        constraints (str): Optional constraints for the code generation.
    
    Returns:
        str: The generated code.
    """
    context = f"You are an expert {language} programmer. Generate high-quality {language} code based on the following instructions."
    prompt = f"{context}\n\nInstructions: {instructions}\n\nImportant: Respond ONLY with the raw {language} code. Do not include markdown code blocks (```), explanations, comments, or any text outside the code. The code must be syntactically correct and properly indented. No introductions or conclusions.\n"
    if constraints:
        prompt += f"Constraints: {constraints}\n"
    code = send_prompt(prompt)
    logging.info(f"Generated code for instructions: {instructions[:50]}...")
    
    code = clean_code_output(code)
    
    # Format with black if Python
    if language.lower() == "python":
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            subprocess.run(['black', temp_file], capture_output=True)
            with open(temp_file, 'r') as f:
                code = f.read()
            os.unlink(temp_file)
        except Exception:
            pass  # If black fails, use original
    
    return code

def generate_tests(code, language="Python"):
    """
    Generate tests for the given code using AI.
    
    Args:
        code (str): The code to test.
        language (str): The programming language.
    
    Returns:
        str: The generated test code.
    """
    if language.lower() != "python":
        return ""  # Only support Python tests for now
    
    prompt = f"Write comprehensive pytest tests for the following Python code. Include edge cases and ensure the tests are complete and correct.\n\nCode:\n{code}\n\nRespond ONLY with the raw Python test code. Do not include markdown, explanations, or any text outside the code. Start directly with imports and test functions."
    test_code = send_prompt(prompt)
    logging.info(f"Generated tests for code snippet")
    
    test_code = clean_code_output(test_code)
    
    # Format with black
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_code)
            temp_file = f.name
        subprocess.run(['black', temp_file], capture_output=True)
        with open(temp_file, 'r') as f:
            test_code = f.read()
        os.unlink(temp_file)
    except Exception:
        pass
    
    return test_code

def save_to_history(instructions, code, file_path):
    """Save generation history to a file."""
    with open('ai_history.txt', 'a') as f:
        f.write(f"Instructions: {instructions}\nFile: {file_path}\nCode:\n{code}\n---\n")
    logging.info(f"Saved generation history for {file_path}")

def generate_and_write_code(instructions, file_path, language="Python", constraints=None, generate_tests_flag=True):
    """
    Generate code using the local AI and write it to a file with safeguards.
    Optionally generates and writes tests.
    
    Args:
        instructions (str): The coding task description.
        file_path (str): The path to the file where code will be written.
        language (str): The programming language, default is 'Python'.
        constraints (str): Optional constraints for the code generation.
        generate_tests_flag (bool): Whether to generate tests, default True.
    
    Returns:
        str: Status message indicating success or error.
    """
    code = generate_code(instructions, language, constraints)
    
    # Validate syntax for Python
    if language.lower() == "python":
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            return f"Syntax error in generated code: {e}\nGenerated code:\n{code}"
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Check if file exists and create backup
    if os.path.exists(file_path):
        backup_path = file_path + ".bak"
        os.rename(file_path, backup_path)
        print(f"Backup created: {backup_path}")
    
    # Write the code
    save_to_history(instructions, code, file_path)
    logging.info(f"Writing code to {file_path}")
    with open(file_path, 'w') as f:
        f.write(code)
    
    # Generate and write tests
    if generate_tests_flag and language.lower() == "python":
        test_code = generate_tests(code, language)
        if test_code:
            # Determine test file path
            base_name = os.path.basename(file_path)
            test_name = f"test_{base_name}"
            test_dir = os.path.join(os.path.dirname(file_path), "..", "tests")
            test_path = os.path.join(test_dir, test_name)
            os.makedirs(os.path.dirname(test_path), exist_ok=True)
            
            # Backup if exists
            if os.path.exists(test_path):
                backup_path = test_path + ".bak"
                os.rename(test_path, backup_path)
                print(f"Test backup created: {backup_path}")
            
            with open(test_path, 'w') as f:
                f.write(test_code)
            logging.info(f"Tests written to {test_path}")
            print(f"Tests written to {test_path}")
    
    return f"Code successfully written to {file_path}"
