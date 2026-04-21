import requests
import os

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
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        return f"Error communicating with Ollama: {e}"

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
    prompt = f"{context}\n\nInstructions: {instructions}\n\nExpected Output: Provide only the raw {language} code without any markdown formatting, comments, explanations, or extra whitespace. Start directly with the code.\n"
    if constraints:
        prompt += f"Constraints: {constraints}\n"
    code = send_prompt(prompt)
    # Clean the code
    code = code.strip()
    # Remove any leading common indentation
    lines = code.split('\n')
    if lines:
        # Find the minimum indentation of non-empty lines
        min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
        code = '\n'.join(line[min_indent:] if line.strip() else line for line in lines)
    return code

def generate_and_write_code(instructions, file_path, language="Python", constraints=None):
    """
    Generate code using the local AI and write it to a file with safeguards.
    
    Args:
        instructions (str): The coding task description.
        file_path (str): The path to the file where code will be written.
        language (str): The programming language, default is 'Python'.
        constraints (str): Optional constraints for the code generation.
    
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
    with open(file_path, 'w') as f:
        f.write(code)
    
    return f"Code successfully written to {file_path}"
