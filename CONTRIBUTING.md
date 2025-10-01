# Contributing to Distributed Anomaly Detection System

Thank you for your interest in contributing to this project! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### 1. Fork and Clone
```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/Distributed-Anomaly-Detection-Using-Machine-Learning-Techniques.git
cd Distributed-Anomaly-Detection-Using-Machine-Learning-Techniques
```

### 2. Set Up Development Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install pytest pytest-cov flake8 black
```

### 3. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

## 📝 Development Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Use type hints where appropriate
- Keep functions focused and modular

### Code Quality
- Write unit tests for new functionality
- Ensure all tests pass before submitting PR
- Maintain or improve code coverage
- Use descriptive commit messages

### Example Code Structure
```python
from typing import List, Dict, Optional

def calculate_energy_efficiency(nodes: List[Node]) -> float:
    """
    Calculate the overall energy efficiency of the network.
    
    Args:
        nodes: List of Node objects in the network
        
    Returns:
        Float representing efficiency (0.0 to 1.0)
        
    Raises:
        ValueError: If nodes list is empty
    """
    if not nodes:
        raise ValueError("Nodes list cannot be empty")
    
    # Implementation here
    pass
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=distributed_anomaly_detection

# Run specific test file
python -m pytest tests/test_system.py -v
```

### Writing Tests
- Write tests for all new functionality
- Follow the existing test structure
- Use descriptive test names
- Include edge cases and error conditions

## 📋 Types of Contributions

### 🐛 Bug Fixes
- Check existing issues first
- Create an issue if none exists
- Include steps to reproduce
- Provide a clear solution

### ✨ New Features
- Discuss major changes in issues first
- Ensure features align with project goals
- Include comprehensive tests
- Update documentation

### 📚 Documentation
- Fix typos and grammatical errors
- Improve code comments
- Add examples and tutorials
- Update README files

### 🔧 Performance Improvements
- Include benchmarks showing improvement
- Ensure no functionality is broken
- Document the optimization approach

## 🎯 Areas Where Help Is Needed

### High Priority
- [ ] **Real-time Implementation**: Adapt for real IoT hardware
- [ ] **Advanced ML Models**: Implement neural networks or ensemble methods
- [ ] **Security Enhancements**: Add cryptographic features
- [ ] **Performance Optimization**: Improve scalability for large networks

### Medium Priority
- [ ] **Visualization Dashboard**: Web-based monitoring interface
- [ ] **Configuration GUI**: User-friendly parameter tuning
- [ ] **Additional Attack Types**: Expand anomaly detection capabilities
- [ ] **Mobile Node Support**: Handle dynamic network topology

### Documentation & Testing
- [ ] **API Documentation**: Generate comprehensive API docs
- [ ] **Integration Tests**: End-to-end system testing
- [ ] **Performance Benchmarks**: Establish baseline metrics
- [ ] **Tutorial Videos**: Create educational content

## 🚀 Submission Process

### 1. Before Submitting
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] Branch is up to date with main

### 2. Pull Request Checklist
- [ ] **Title**: Clear, descriptive PR title
- [ ] **Description**: Explain what and why
- [ ] **Issue Link**: Reference related issues
- [ ] **Tests**: Include or update tests
- [ ] **Documentation**: Update relevant docs

### 3. PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Performance improvement
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

## 🔍 Code Review Process

### What We Look For
- **Functionality**: Does it work as expected?
- **Code Quality**: Is it readable and maintainable?
- **Testing**: Are there adequate tests?
- **Documentation**: Is it properly documented?
- **Performance**: Does it maintain or improve performance?

### Review Timeline
- Initial review: Within 48 hours
- Follow-up reviews: Within 24 hours
- Merge decision: Within 1 week

## 🎨 Coding Standards

### Python Standards
```python
# Good
def calculate_network_efficiency(
    nodes: List[Node], 
    time_window: int = 10
) -> Dict[str, float]:
    """Calculate efficiency metrics for the network."""
    pass

# Avoid
def calc_eff(nodes, time=10):
    pass
```

### Configuration Changes
```python
# Update config.py for new parameters
NEW_FEATURE_ENABLED = True
NEW_FEATURE_THRESHOLD = 0.75

# Add to relevant docstrings
# Document in README.md if user-facing
```

### Error Handling
```python
# Good
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    return default_value

# Avoid bare except clauses
except:
    pass
```

## 📞 Getting Help

### Communication Channels
- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Pull Request Comments**: For code-specific discussions

### Before Asking for Help
1. Check existing issues and documentation
2. Search previous discussions
3. Try to isolate the problem
4. Provide minimal reproducible example

### When Reporting Issues
- **Environment**: Python version, OS, dependencies
- **Steps**: How to reproduce the issue
- **Expected**: What should happen
- **Actual**: What actually happens
- **Logs**: Relevant error messages or logs

## 🏆 Recognition

Contributors will be:
- Added to the README contributors section
- Mentioned in release notes for significant contributions
- Eligible for maintainer status based on consistent contributions

## 📄 License Agreement

By contributing, you agree that your contributions will be licensed under the same MIT License that covers the project.

---

Thank you for contributing! 🎉

**Happy coding!** 🚀