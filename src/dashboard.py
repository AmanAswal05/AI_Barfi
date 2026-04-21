from flask import Flask, request, render_template_string
import os
import sys

# Add project paths
sys.path.insert(0, os.path.dirname(__file__))

from orchestrator import orchestrator
from logger import logger

app = Flask(__name__)

# Simple HTML template
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Code Generator Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        form { max-width: 600px; }
        textarea { width: 100%; height: 100px; }
        input[type="text"] { width: 100%; padding: 8px; margin: 5px 0; }
        input[type="submit"] { padding: 10px 20px; background: #007acc; color: white; border: none; cursor: pointer; }
        .message { margin-top: 20px; padding: 10px; border-radius: 5px; }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <h1>AI Code Generator Dashboard</h1>
    <form method="post">
        <label for="file_path">File Path:</label><br>
        <input type="text" id="file_path" name="file_path" required placeholder="e.g., src/utils.py"><br><br>
        
        <label for="instructions">Instructions:</label><br>
        <textarea id="instructions" name="instructions" required placeholder="Describe what code to generate"></textarea><br><br>
        
        <label for="constraints">Constraints (optional):</label><br>
        <input type="text" id="constraints" name="constraints" placeholder="e.g., Use built-in functions only"><br><br>
        
        <input type="submit" value="Generate Code">
    </form>
    {% if message %}
    <div class="message {{ 'success' if 'successfully' in message else 'error' }}">
        {{ message }}
    </div>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    if request.method == 'POST':
        file_path = request.form['file_path']
        instructions = request.form['instructions']
        constraints = request.form.get('constraints', '').strip()
        
        logger.info(f"Dashboard request: {file_path} - {instructions[:50]}...")
        
        # Generate code
        success = orchestrator.process_task(
            file_path=file_path,
            instructions=instructions,
            constraints=constraints if constraints else None
        )
        
        if success:
            message = f"Code successfully generated and committed for {file_path}"
        else:
            message = "Failed to generate code. Check logs for details."
    
    return render_template_string(TEMPLATE, message=message)

if __name__ == '__main__':
    logger.info("Starting Flask dashboard")
    app.run(debug=True, host='0.0.0.0', port=5000)
