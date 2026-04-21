# AI-Powered Code Generation Assistant

A clean, modular, and maintainable local AI-powered coding assistant that integrates smoothly with version-controlled projects. Uses Ollama for local AI model inference with robust error handling and safety measures.

## Features

- **Modular Architecture**: Clean separation of concerns (AI logic, Git automation, orchestration, utilities)
- **Environment Configuration**: All settings via environment variables with validation
- **Robust Error Handling**: Model fallbacks, timeout handling, graceful degradation
- **Safe File Operations**: Validation, backups, and meaningful change detection
- **Intelligent Git Integration**: Context-aware commit messages, test validation before commits
- **Web Dashboard**: Flask-based interface for interactive code generation
- **Comprehensive Logging**: Structured logging with configurable levels
- **Automated Testing**: Built-in test suite for reliability verification
- **Docker Support**: Containerized deployment for portability

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables** (optional):
   ```bash
   export OLLAMA_BASE_URL="http://localhost:11434"
   export PRIMARY_MODEL="codellama"
   export LOG_LEVEL="INFO"
   ```

3. **Install and Start Ollama**:
   ```bash
   # Install from https://ollama.ai
   ollama pull codellama
   ollama serve
   ```

4. **Run Tests**:
   ```bash
   python -m pytest tests/
   ```

## Usage

### Command Line Interface

**Monitor Tasks**:
```bash
python scripts/monitor_tasks.py
```
Add tasks to `tasks.txt` in format: `file_path | instructions | constraints`

**Auto-Commit**:
```bash
python scripts/auto_commit.py
```

**Update Models**:
```bash
python scripts/update_model.py --model codellama
```

### Web Dashboard

```bash
python src/dashboard.py
```
Open http://localhost:5000 for interactive code generation.

### Programmatic Usage

```python
from src.orchestrator import orchestrator

success = orchestrator.process_task(
    file_path="src/utils.py",
    instructions="Write a function to calculate factorial",
    constraints="Use recursion"
)
```

## Project Structure

```
my_project/
├── src/                    # Core modules
│   ├── __init__.py        # Package initialization
│   ├── config.py          # Environment configuration
│   ├── logger.py          # Logging setup
│   ├── ai_client.py       # AI model interaction
│   ├── code_generator.py  # Code generation and cleaning
│   ├── file_handler.py    # Safe file operations
│   ├── git_manager.py     # Git automation
│   ├── orchestrator.py    # Main workflow coordination
│   ├── utils.py           # Utility functions
│   └── dashboard.py       # Web interface
├── scripts/               # Automation scripts
│   ├── monitor_tasks.py   # Task monitoring
│   ├── auto_commit.py     # Auto-commit workflow
│   └── update_model.py    # Model updates
├── tests/                 # Test suite
│   ├── test_config.py     # Configuration tests
│   └── test_utils.py      # Utility tests
├── ai_assistant.log       # Application logs
├── ai_history.txt         # Generation history
├── tasks.txt              # Task queue
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
└── docker-compose.yml     # Compose setup
```

## Configuration

Configure via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama API endpoint |
| `PRIMARY_MODEL` | `codellama` | Primary AI model |
| `FALLBACK_MODEL` | `llama3.2` | Fallback model |
| `LOG_LEVEL` | `INFO` | Logging level |
| `LOG_FILE` | `ai_assistant.log` | Log file path |
| `BACKUP_SUFFIX` | `.bak` | File backup suffix |
| `GIT_REMOTE` | `origin` | Git remote name |
| `GIT_BRANCH` | `main` | Git branch |
| `CACHE_ENABLED` | `false` | Enable response caching |
| `CACHE_DIR` | `.ai_cache` | Cache directory |

## Docker Deployment

```bash
# Build and run
docker-compose up --build

# Or run specific services
docker-compose up ai-dashboard
docker-compose up ollama
```

## Development

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=src/

# Run specific test
python -m pytest tests/test_config.py
```

### Code Quality

```bash
# Format code
black src/ scripts/ tests/

# Type checking (if mypy configured)
mypy src/
```

### Maintenance Tasks

- **Update Models**: Run `python scripts/update_model.py` periodically
- **Review Logs**: Check `ai_assistant.log` for issues
- **Clean History**: Archive old `ai_history.txt` entries
- **Backup**: Files are automatically backed up with `.bak` suffix
- **Monitor Performance**: Ensure Ollama models are responsive

## Safety & Best Practices

- **Code Validation**: All generated code is syntax-validated before writing
- **Backup Creation**: Existing files are backed up before modification
- **Test Requirements**: Tests must pass before commits
- **Meaningful Commits**: Only commits when there are actual changes
- **Error Handling**: Graceful fallbacks for model failures
- **No Auto-Execution**: Generated code is never automatically executed
- **Clean Prompts**: AI prompts designed to produce clean, focused output

## API Reference

### Core Classes

- **`Config`**: Configuration management
- **`AIClient`**: AI model interaction with fallbacks
- **`CodeGenerator`**: Code generation and formatting
- **`FileHandler`**: Safe file operations
- **`GitManager`**: Git automation
- **`TaskOrchestrator`**: Main workflow coordination

### Key Functions

- `orchestrator.process_task()`: Process a single coding task
- `orchestrator.auto_commit_workflow()`: Complete auto-commit process
- `code_generator.generate_code()`: Generate code from instructions
- `file_handler.write_code_file()`: Safely write code to file

## Troubleshooting

### Common Issues

1. **Ollama Connection Failed**
   - Ensure Ollama is running: `ollama serve`
   - Check `OLLAMA_BASE_URL` configuration

2. **Model Not Available**
   - Pull model: `ollama pull codellama`
   - Check model name in configuration

3. **Tests Failing**
   - Run tests manually: `python -m pytest tests/`
   - Check test requirements and syntax

4. **Git Operations Failing**
   - Ensure repository is initialized
   - Check Git credentials and remote configuration

### Logs and Debugging

- Check `ai_assistant.log` for detailed error information
- Set `LOG_LEVEL=DEBUG` for verbose logging
- Review `ai_history.txt` for generation history

## Contributing

1. Follow the modular structure
2. Add tests for new functionality
3. Update documentation
4. Ensure all tests pass
5. Use meaningful commit messages

## License

This project is provided as-is for educational and development purposes.
