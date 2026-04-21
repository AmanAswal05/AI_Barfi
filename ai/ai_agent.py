import requests

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
