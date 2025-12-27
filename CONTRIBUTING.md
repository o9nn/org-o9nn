# Contributing to O9NN Organization

Thank you for your interest in contributing to the O9NN organization! This document provides guidelines for contributing to the `org-o9nn` meta-repository.

## 🎯 Ways to Contribute

### 1. Improve Analysis Scripts
- Enhance data processing algorithms
- Add new metrics and insights
- Optimize performance
- Fix bugs

### 2. Enhance Visualizations
- Create new chart types
- Improve visual design
- Add interactive elements
- Support additional export formats

### 3. Expand Documentation
- Improve README clarity
- Add usage examples
- Create tutorials
- Document best practices

### 4. Add Features
- New GitHub API integrations
- Additional analysis dimensions
- Automated reporting
- Integration with other tools

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- GitHub account
- GitHub Personal Access Token (for testing)

### Setup Development Environment

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/org-o9nn.git
cd org-o9nn

# Add upstream remote
git remote add upstream https://github.com/o9nn/org-o9nn.git

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export GITHUB_TOKEN="your_test_token"
export ORG_LOGIN="o9nn"
```

## 📝 Development Workflow

### 1. Create a Feature Branch

```bash
# Update your main branch
git checkout main
git pull upstream main

# Create a feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Write clean, readable code
- Follow existing code style
- Add comments for complex logic
- Update documentation as needed

### 3. Test Your Changes

```bash
# Test syntax
make test

# Run individual scripts
python fetch_org_graph.py
python analyze_org.py
python visualize_graph.py

# Or run all at once
make all
```

### 4. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "feat: add new analysis metric for repository activity"
```

**Commit Message Format:**

```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

### 5. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create a Pull Request on GitHub
```

## 🎨 Code Style Guidelines

### Python Code

Follow [PEP 8](https://pep8.org/) style guide:

```python
# Good
def fetch_organization_data(org_login, github_token):
    """
    Fetch organization data from GitHub GraphQL API.
    
    Args:
        org_login: GitHub organization login name
        github_token: GitHub personal access token
        
    Returns:
        Complete organization data dictionary
    """
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Content-Type": "application/json"
    }
    # ... implementation
```

**Key Points:**
- Use 4 spaces for indentation
- Maximum line length: 120 characters
- Use descriptive variable names
- Add docstrings to all functions
- Include type hints where appropriate

### JSON Files

```json
{
  "key": "value",
  "nested": {
    "indent": 2
  }
}
```

- Use 2 spaces for indentation
- Keep structure consistent

### Markdown Files

- Use ATX-style headers (`#`, `##`, etc.)
- Add blank lines around headers
- Use code blocks with language specification
- Keep line length reasonable (80-100 chars)

## 🧪 Testing Guidelines

### Manual Testing

Before submitting a PR, test:

1. **Syntax Check**
   ```bash
   make test
   ```

2. **Functionality Test**
   ```bash
   make all
   ```

3. **Visual Inspection**
   - Check generated PNG files
   - Verify JSON structure
   - Review analysis output

### Test Cases to Consider

- Empty organization data
- Missing fields in API response
- Network errors
- Invalid tokens
- Large datasets (100+ repos)

## 📋 Pull Request Guidelines

### Before Submitting

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No unnecessary files included

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Other (please describe)

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
Describe how you tested your changes

## Screenshots (if applicable)
Add screenshots for visual changes

## Related Issues
Closes #issue_number
```

### Review Process

1. Automated checks will run
2. Maintainers will review your code
3. Address any feedback
4. Once approved, your PR will be merged

## 🐛 Reporting Bugs

### Before Reporting

- Check existing issues
- Verify it's reproducible
- Gather relevant information

### Bug Report Template

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.11.0]
- Dependencies: [output of `pip list`]

## Additional Context
Any other relevant information
```

## 💡 Feature Requests

### Feature Request Template

```markdown
## Feature Description
Clear description of the proposed feature

## Use Case
Why is this feature needed?

## Proposed Solution
How should it work?

## Alternatives Considered
Other approaches you've thought about

## Additional Context
Any other relevant information
```

## 📚 Documentation Contributions

### Types of Documentation

- **Code Comments** - Inline explanations
- **Docstrings** - Function/class documentation
- **README** - Overview and quick start
- **Tutorials** - Step-by-step guides
- **API Docs** - Detailed reference

### Documentation Style

- Use clear, concise language
- Include examples
- Keep it up-to-date
- Add diagrams where helpful

## 🔒 Security

### Reporting Security Issues

**DO NOT** open public issues for security vulnerabilities.

Instead:
1. Email the maintainers directly
2. Provide detailed description
3. Include steps to reproduce
4. Suggest a fix if possible

### Security Best Practices

- Never commit tokens or secrets
- Use environment variables
- Validate all inputs
- Handle errors gracefully

## 🤝 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on constructive feedback
- Help others learn and grow

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information

## 📞 Getting Help

### Resources

- **Documentation:** [README.md](README.md)
- **Discussions:** [GitHub Discussions](https://github.com/o9nn/org-o9nn/discussions)
- **Issues:** [GitHub Issues](https://github.com/o9nn/org-o9nn/issues)

### Questions?

- Check existing documentation
- Search closed issues
- Ask in GitHub Discussions
- Open a new issue if needed

## 🎉 Recognition

Contributors will be:
- Listed in release notes
- Mentioned in CHANGELOG
- Credited in documentation
- Appreciated by the community!

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to O9NN! 🚀
