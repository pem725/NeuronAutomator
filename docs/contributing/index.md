# Contributing

Thank you for your interest in contributing to Neuron Daily Newsletter Automation! This project welcomes contributions from the community.

## 🚀 Quick Start for Contributors

### Getting Started
```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/NeuronAutomator.git
cd NeuronAutomator

# 3. Set up development environment
python3 -m venv dev-env
source dev-env/bin/activate  # Linux/macOS
# dev-env\Scripts\activate     # Windows

# 4. Install dependencies
pip install -r requirements.txt
pip install -r docs-requirements.txt

# 5. Make your changes
# 6. Test your changes
python neuron_automation.py --test

# 7. Submit a pull request
```

## 🎯 Ways to Contribute

### 🐛 Bug Reports
Found a bug? Please report it:

1. **Check existing issues** first
2. **Use the issue template**
3. **Include system information**:
   - OS and version
   - Python version  
   - Chrome version
   - Error messages and logs

### ✨ Feature Requests
Have an idea for improvement?

1. **Check the roadmap** in [TODO.md](../../TODO.md)
2. **Describe the use case** clearly
3. **Explain the benefit** to users
4. **Consider implementation complexity**

### 📝 Documentation Improvements
Documentation can always be better:

- Fix typos and grammar
- Add examples and clarifications
- Improve mobile formatting
- Translate to other languages

### 🛠️ Code Contributions
Code contributions are welcome:

- Bug fixes
- New features
- Performance improvements
- Test coverage
- Code cleanup

## 📋 Development Guidelines

### Code Style
```python
# Follow PEP 8 style guide
# Use descriptive variable names
# Add docstrings to functions
# Keep functions focused and small

def get_newsletter_links(url: str) -> List[str]:
    """
    Extract article links from newsletter page.
    
    Args:
        url: Newsletter page URL
        
    Returns:
        List of article URLs found
    """
    # Implementation here
```

### Testing
```bash
# Run basic tests
python neuron_automation.py --test

# Test browser integration
python neuron_automation.py --test-browser

# Test configuration
python neuron_automation.py --check-config

# Test time rewind
python blacklist_rewind.py --test
```

### Documentation
- Update relevant `.md` files
- Test documentation builds:
```bash
# Install docs dependencies
pip install -r docs-requirements.txt

# Build documentation
python -m mkdocs serve

# Check for broken links
python -m mkdocs build --strict
```

## 🗂️ Project Structure

### Core Files
```
neuron_automation.py        # Main automation script
link_manager.py            # Link management and blacklisting  
blacklist_rewind.py        # Time rewind functionality
config.py                  # Configuration management
```

### Documentation
```
docs/                      # MkDocs documentation
├── index.md              # Homepage
├── installation/         # Installation guides  
├── features/             # Feature documentation
├── configuration/        # Config guides
├── usage/                # Usage instructions
└── reference/            # Technical reference
```

### Infrastructure
```
.github/workflows/        # GitHub Actions CI/CD
installers/              # Platform-specific installers
requirements.txt         # Python dependencies
docs-requirements.txt    # Documentation dependencies  
mkdocs.yml              # Documentation configuration
netlify.toml            # Netlify deployment config
```

## 🔧 Development Setup

### Local Testing Environment
```bash
# Create test configuration
cp config.py config-test.py

# Edit test config for development
class DevelopmentConfig(Config):
    LOG_LEVEL = "DEBUG"
    ENABLED_DAYS = [0, 1, 2, 3, 4, 5, 6]  # Every day for testing
    AUTOMATION_TIMES = ["10:00"]  # Single test time
    HEADLESS_MODE = False  # See what's happening
    
# Use test config
export NEURON_CONFIG_FILE="config-test.py"
```

### Running Tests
```bash
# Basic functionality test
python neuron_automation.py --dry-run

# Full system test  
python neuron_automation.py --test --verbose

# Browser integration test
python neuron_automation.py --test-browser

# Database operations test
python link_manager.py --test

# Time rewind test
python blacklist_rewind.py --test
```

## 🚢 Deployment and Release

### Documentation Updates
Documentation is automatically deployed when you push to `main`:

1. **Edit documentation** in `docs/` folder
2. **Test locally**: `python -m mkdocs serve`
3. **Commit changes**: `git commit -m "docs: update installation guide"`  
4. **Push**: `git push origin main`
5. **Auto-deploy**: GitHub Actions builds and deploys

### Versioning
We use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible  
- **PATCH**: Bug fixes, backward compatible

### Release Process
1. Update version in `setup.py` and `neuron_automation.py`
2. Update CHANGELOG.md
3. Create release on GitHub
4. CI automatically builds and publishes

## 📝 Pull Request Guidelines

### Before Submitting
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated if needed
- [ ] Commit messages are descriptive
- [ ] Changes are focused and atomic

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature  
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Tests pass locally
- [ ] Tested on [OS/Platform]
- [ ] Manual testing completed

## Checklist  
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

## 🏷️ Issue Labels

We use these labels to categorize issues:

| Label | Purpose |
|-------|---------|
| `bug` | Something isn't working |
| `enhancement` | New feature or request |
| `documentation` | Documentation improvements |  
| `good first issue` | Good for new contributors |
| `help wanted` | Extra attention needed |
| `platform:linux` | Linux-specific issue |
| `platform:macos` | macOS-specific issue |
| `platform:windows` | Windows-specific issue |

## 🎉 Recognition

Contributors are recognized in:

- **README.md** contributors section
- **GitHub contributors** page  
- **Release notes** for significant contributions
- **Documentation credits**

### Hall of Fame
Major contributors who have significantly improved the project:

- **AI Assistant & pem725**: Original development and architecture
- _(Your name here!)_

## 🆘 Getting Help

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and community chat
- **Documentation**: Comprehensive guides and references

### Development Questions
- Check existing **GitHub Issues** and **Discussions**
- Review the **Technical Reference** documentation
- Look at **recent commits** for context
- Ask specific questions with **code examples**

## 🎯 Roadmap

Check [TODO.md](../../TODO.md) for:
- **Current priorities**
- **Future enhancements** 
- **Community wishes**
- **Technical debt items**

Popular requested features:
- Multi-newsletter support
- RSS feed integration
- Mobile app companion
- Cloud sync capabilities
- Advanced analytics dashboard

---

## Thank You! 🙏

Every contribution makes this project better. Whether you're fixing a typo, reporting a bug, suggesting a feature, or contributing code - **thank you for being part of the Neuron Automation community!**

Ready to contribute? **[Check out our issues](https://github.com/pem725/NeuronAutomator/issues)** labeled "good first issue" to get started!