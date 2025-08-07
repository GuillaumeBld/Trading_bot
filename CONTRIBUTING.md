# Contributing to AI-Powered Trading Bot

Thank you for your interest in contributing to the AI-Powered Trading Bot! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/Trading_bot.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit your changes: `git commit -m "Add your feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/GuillaumeBld/Trading_bot.git
cd Trading_bot

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (if available)
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Write tests for new features

## Pull Request Guidelines

- Ensure all tests pass
- Add tests for new features
- Update documentation as needed
- Keep commits focused and atomic
- Write clear commit messages

## Reporting Issues

When reporting issues, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Relevant error messages

## Security

Never commit:
- API keys or secrets
- Personal trading data
- Sensitive configuration files

Use environment variables for sensitive data.

## Questions?

Feel free to open an issue for questions or join our discussions.

Thank you for contributing!