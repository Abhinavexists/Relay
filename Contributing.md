# Contributing to Workflow Automation System

Thank you for your interest in contributing to the Workflow Automation System! This document provides guidelines and instructions for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Contributions](#making-contributions)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)

## 📜 Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

- Be respectful and inclusive
- Exercise consideration and empathy
- Focus on what is best for the community
- Use welcoming and inclusive language
- Be collaborative
- Gracefully accept constructive criticism

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/workflow-automation.git
   cd workflow-automation
   ```
3. Add the upstream remote:
   ```bash
   git remote add upstream https://github.com/original-owner/workflow-automation.git
   ```

## 💻 Development Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

3. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

## 🛠️ Making Contributions

### Branch Naming Convention

- Feature: `feature/description`
- Bug fix: `fix/description`
- Documentation: `docs/description`
- Performance: `perf/description`

### Commit Message Guidelines

Format:
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Code style changes (formatting, etc.)
- refactor: Code refactoring
- perf: Performance improvements
- test: Adding or modifying tests
- chore: Maintenance tasks

Example:
```
feat(telegram): add new workflow command

Add /workflow_status command to check current workflow status.

Closes #123
```

## 📥 Pull Request Process

1. Update your fork:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. Make your changes and commit them:
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

4. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

5. Create a Pull Request through GitHub

### PR Requirements

- [ ] Tests added/updated for new features
- [ ] Documentation updated
- [ ] Code follows project style guidelines
- [ ] All tests passing
- [ ] PR description clearly explains changes
- [ ] Linked to relevant issues

## 📝 Coding Standards

### Python Style Guide

- Follow PEP 8 guidelines
- Use type hints
- Maximum line length: 88 characters
- Use docstrings for functions and classes

### Tools

- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

## ✅ Testing Guidelines

1. Write tests for new features:
   ```python
   def test_new_feature():
       # Arrange
       input_data = ...
       
       # Act
       result = feature_function(input_data)
       
       # Assert
       assert result == expected_output
   ```

2. Run tests:
   ```bash
   pytest
   ```

3. Check coverage:
   ```bash
   pytest --cov=.
   ```

## 📚 Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions/classes
- Update API documentation for endpoint changes
- Include example usage where appropriate

## 🐛 Issue Reporting

### Bug Reports

Include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- System information
- Relevant logs/screenshots

### Feature Requests

Include:
- Clear description of the feature
- Use case and benefits
- Possible implementation approach
- Any potential challenges

## 🤝 Getting Help

- Join our [Discord community](link-to-discord)
- Check existing issues and discussions
- Reach out to maintainers
- Review documentation

## 📄 License

By contributing, you agree that your contributions will be licensed under the project's MIT License.

## 🙏 Recognition

Contributors will be added to the [CONTRIBUTORS.md](CONTRIBUTORS.md) file. Thank you for helping improve the Workflow Automation System! 
