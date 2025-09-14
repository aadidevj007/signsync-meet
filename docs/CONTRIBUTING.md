# Contributing to SignSync Meet

Thank you for your interest in contributing to SignSync Meet! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Documentation](#documentation)
- [Community](#community)

## Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow. Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting Started

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **Git** for version control
- **Firebase** account (for testing)
- **Google Cloud** account (for AI services)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/signsync-meet.git
   cd signsync-meet
   ```

3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/original-username/signsync-meet.git
   ```

## Development Setup

### 1. Frontend Setup

```bash
cd frontend
npm install
cp env.example .env
# Edit .env with your Firebase credentials
npm start
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
cp env.example .env
# Edit .env with your API keys
python main.py
```

### 3. AI Models Setup

```bash
cd ai-model
pip install -r requirements.txt
python setup_vosk.py
python train_sign_language_model.py
```

### 4. Database Setup

1. Create a Firebase project
2. Enable Authentication and Firestore
3. Configure security rules
4. Update environment variables

## Contributing Guidelines

### Types of Contributions

We welcome various types of contributions:

- **Bug Fixes**: Fix existing issues
- **Feature Development**: Add new functionality
- **Documentation**: Improve or add documentation
- **Testing**: Add or improve tests
- **Performance**: Optimize existing code
- **UI/UX**: Improve user interface and experience
- **AI Models**: Enhance or add new AI capabilities

### Development Workflow

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-number
   ```

2. **Make Changes**
   - Write clean, readable code
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation

3. **Test Your Changes**
   ```bash
   # Frontend tests
   cd frontend && npm test
   
   # Backend tests
   cd backend && pytest
   
   # AI model tests
   cd ai-model && python -m pytest
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

### Code Style

#### Frontend (React/JavaScript)

- Use **ESLint** and **Prettier** for code formatting
- Follow **React** best practices
- Use **TypeScript** for type safety
- Follow **TailwindCSS** conventions

```javascript
// Good example
const UserProfile = ({ user, onUpdate }) => {
  const [isEditing, setIsEditing] = useState(false);
  
  const handleSave = useCallback(async (data) => {
    try {
      await onUpdate(data);
      setIsEditing(false);
    } catch (error) {
      console.error('Error updating profile:', error);
    }
  }, [onUpdate]);
  
  return (
    <div className="glass-card rounded-2xl p-6">
      {/* Component content */}
    </div>
  );
};
```

#### Backend (Python)

- Follow **PEP 8** style guide
- Use **type hints** for function parameters and return values
- Write **docstrings** for functions and classes
- Use **async/await** for asynchronous operations

```python
# Good example
async def transcribe_audio(
    audio_data: bytes, 
    language: str = "en"
) -> Optional[str]:
    """
    Transcribe audio data to text using voice recognition.
    
    Args:
        audio_data: Raw audio data bytes
        language: Language code for transcription
        
    Returns:
        Transcribed text or None if transcription fails
    """
    try:
        # Implementation
        pass
    except Exception as e:
        logger.error(f"Error transcribing audio: {str(e)}")
        return None
```

#### AI Models (Python)

- Use **NumPy** and **TensorFlow** best practices
- Document model architecture and training process
- Include performance metrics and evaluation results
- Use **MediaPipe** for computer vision tasks

```python
# Good example
class SignLanguageRecognizer:
    """
    Sign language recognition using MediaPipe and CNN.
    
    This class provides real-time sign language recognition
    using computer vision and deep learning models.
    """
    
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = self.load_model()
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
    
    def recognize(self, image: np.ndarray) -> Optional[str]:
        """Recognize sign language from image."""
        # Implementation
        pass
```

### Commit Message Format

Use conventional commit messages:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(auth): add Google OAuth integration
fix(captions): resolve real-time caption delay issue
docs(api): update API documentation for new endpoints
test(ai): add unit tests for sign language recognition
```

## Pull Request Process

### Before Submitting

1. **Update Documentation**
   - Update README if needed
   - Add/update API documentation
   - Include code comments

2. **Add Tests**
   - Unit tests for new functionality
   - Integration tests for API endpoints
   - End-to-end tests for user workflows

3. **Check Code Quality**
   - Run linters and formatters
   - Ensure all tests pass
   - Check for security vulnerabilities

4. **Update Dependencies**
   - Update package.json or requirements.txt
   - Test with updated dependencies
   - Document breaking changes

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
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

### Review Process

1. **Automated Checks**
   - CI/CD pipeline runs
   - Code quality checks
   - Security scans
   - Test coverage

2. **Manual Review**
   - Code review by maintainers
   - Functionality testing
   - Performance evaluation
   - Security assessment

3. **Approval and Merge**
   - At least one approval required
   - All checks must pass
   - Maintainer merges PR

## Issue Reporting

### Bug Reports

Use the bug report template:

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g. Windows, macOS, Linux]
- Browser: [e.g. Chrome, Firefox, Safari]
- Version: [e.g. 1.0.0]

**Additional context**
Any other context about the problem.
```

### Feature Requests

Use the feature request template:

```markdown
**Is your feature request related to a problem?**
A clear description of what the problem is.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Alternative solutions or features you've considered.

**Additional context**
Any other context or screenshots about the feature request.
```

## Testing

### Frontend Testing

```bash
# Unit tests
npm test

# E2E tests
npm run test:e2e

# Coverage report
npm run test:coverage
```

### Backend Testing

```bash
# Unit tests
pytest

# Integration tests
pytest tests/integration/

# Coverage report
pytest --cov=backend
```

### AI Model Testing

```bash
# Model tests
python -m pytest tests/

# Performance tests
python tests/performance_test.py
```

### Test Guidelines

- Write tests for all new functionality
- Aim for 80%+ code coverage
- Include both positive and negative test cases
- Test edge cases and error conditions
- Use descriptive test names

## Documentation

### Code Documentation

- Write clear docstrings for functions and classes
- Include type hints for Python code
- Add JSDoc comments for JavaScript/TypeScript
- Document complex algorithms and AI models

### API Documentation

- Update API documentation for new endpoints
- Include request/response examples
- Document error codes and messages
- Add authentication requirements

### User Documentation

- Update README for new features
- Add setup and installation instructions
- Include troubleshooting guides
- Document configuration options

## Community

### Getting Help

- **GitHub Discussions**: For questions and discussions
- **GitHub Issues**: For bug reports and feature requests
- **Discord**: For real-time community chat
- **Email**: For security issues

### Contributing to Documentation

- Fix typos and grammatical errors
- Improve clarity and readability
- Add missing information
- Update outdated content

### Contributing to Tests

- Add test cases for edge cases
- Improve test coverage
- Add performance tests
- Add integration tests

## Recognition

Contributors will be recognized in:
- **README.md**: Contributor list
- **Release Notes**: Feature contributors
- **GitHub**: Contributor statistics
- **Documentation**: Credit for significant contributions

## License

By contributing to SignSync Meet, you agree that your contributions will be licensed under the MIT License.

## Questions?

If you have questions about contributing, please:
1. Check existing issues and discussions
2. Create a new discussion
3. Contact maintainers directly

Thank you for contributing to SignSync Meet! 🎉
