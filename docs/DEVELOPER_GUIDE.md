# Developer Guide - NFL Trivia Quiz

**Version**: 1.0 (MVP)
**Target Audience**: Backend and full-stack developers
**Last Updated**: November 5, 2025

## Table of Contents
1. [Getting Started](#getting-started)
2. [Architecture Deep Dive](#architecture-deep-dive)
3. [Development Workflow](#development-workflow)
4. [Testing Strategy](#testing-strategy)
5. [Security Best Practices](#security-best-practices)
6. [Performance Optimization](#performance-optimization)
7. [Troubleshooting Guide](#troubleshooting-guide)
8. [Contributing Guidelines](#contributing-guidelines)

---

## Getting Started

### Prerequisites
- Python 3.8+ installed
- pip package manager
- Git for version control
- Modern text editor (VS Code, PyCharm, etc.)
- Basic understanding of Flask and web development

### Quick Start
```bash
# Clone repository
git clone https://github.com/rocklambros/nfl-trivia-quiz.git
cd nfl-trivia-quiz

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Validate installation
python3 exam_data.py  # Should output "✅ All 10 questions are valid!"

# Run development server
python3 app.py
```

Access at: `http://127.0.0.1:5000`

### Project Structure
```
nfl-trivia-quiz/
├── app.py                 # Flask application (routing, security, sessions)
├── exam_data.py           # Question bank (dictionary-based storage)
├── grader.py              # Grading algorithms (pure logic, no I/O)
├── requirements.txt       # Python dependencies
├── templates/             # Jinja2 HTML templates
│   ├── index.html         # Exam interface
│   ├── results.html       # Results display
│   └── error.html         # Error pages
├── static/                # Static assets
│   └── style.css          # Responsive CSS with accessibility
├── docs/                  # Documentation
│   ├── API_REFERENCE.md
│   ├── DEVELOPER_GUIDE.md
│   └── DEPLOYMENT.md
├── .gitignore             # Git exclusions
├── README.md              # User documentation
├── PRD.md                 # Product requirements
├── CLAUDE.md              # Claude Code context
└── VALIDATION_REPORT.md   # Quality assurance report
```

---

## Architecture Deep Dive

### Design Philosophy

**Core Principle**: Dictionary-based architecture for educational purposes

The application demonstrates Python dictionary usage as a primary educational objective. All data structures - questions, answers, results - use dictionaries.

### Three-Layer Architecture

#### 1. Presentation Layer (templates/)
**Responsibility**: User interface and client-side interactions

- **index.html**: Exam interface with form, validation, progress tracking
- **results.html**: Score display with question-by-question breakdown
- **error.html**: User-friendly error pages

**Key Features**:
- Semantic HTML5 with ARIA attributes
- Progressive enhancement with vanilla JavaScript
- WCAG 2.1 AA accessibility compliance
- Responsive design (mobile-first approach)

#### 2. Application Layer (app.py)
**Responsibility**: HTTP routing, session management, security controls

**Routes**:
- `GET /` - Display exam
- `POST /submit` - Process answers
- `GET /results` - Show results
- `GET /retake` - Clear session

**Security Controls**:
- Input validation (OWASP A03)
- Session security (OWASP A07)
- Security logging (OWASP A09)
- Error handling (OWASP A05)

#### 3. Business Logic Layer (exam_data.py, grader.py)
**Responsibility**: Data access and grading algorithms

**exam_data.py**:
- Question storage (QUESTIONS constant)
- Data access methods
- Structure validation

**grader.py**:
- Score calculation (percentage-based)
- Answer comparison logic
- Results dictionary generation
- Performance feedback determination

**Critical Characteristic**: Pure functions with no I/O dependencies (testable in isolation)

---

### Data Flow Architecture

```
User Browser
    ↓ (HTTP GET /)
Flask Route: index()
    ↓
exam_data.get_all_questions()
    ↓
Template: index.html
    ↓ (User answers questions)
User Browser
    ↓ (HTTP POST /submit)
Flask Route: submit()
    ↓
validate_answer_input(form_data)
    ↓
sanitize_user_answers(form_data)
    ↓
grader.grade_exam(questions, answers)
    ↓
session['results'] = results
    ↓
Redirect → /results
    ↓
Flask Route: results()
    ↓
Template: results.html
    ↓
User Browser
```

---

### Dictionary Architecture

#### Question Dictionary Pattern
```python
QUESTIONS = {
    "q1": {                      # Question ID (key)
        "question": str,         # Question text
        "options": {             # Nested dictionary for options
            "A": str,
            "B": str,
            "C": str,
            "D": str
        },
        "correct": str           # Correct answer key
    }
}
```

**Design Rationale**:
- O(1) lookup time for questions by ID
- Easy iteration for form rendering
- Natural JSON serialization for future API
- Clear key-value semantics

#### Answer Dictionary Pattern
```python
user_answers = {
    "q1": "B",    # question_id: answer_key
    "q2": "A",
    # ...
}
```

**Design Rationale**:
- Parallel structure to questions dictionary
- Simple comparison logic in grading
- Easy validation (key existence check)
- Minimal memory footprint

#### Results Dictionary Pattern
```python
results = {
    "score": int,              # 0-100
    "correct_count": int,
    "total_questions": int,
    "percentage": float,
    "feedback_message": str,
    "details": {               # Nested dictionary for per-question results
        "q1": {
            "user_answer": str,
            "correct_answer": str,
            "is_correct": bool,
            "question_text": str
        }
    }
}
```

**Design Rationale**:
- Self-contained result object
- Easy template rendering (direct key access)
- Session serialization compatible
- Extensible for future analytics

---

### Session Management Strategy

**Flask Sessions**: Server-side session storage using secure cookies

**Security Configuration**:
```python
SESSION_COOKIE_HTTPONLY=True    # XSS protection
SESSION_COOKIE_SAMESITE='Lax'   # CSRF protection
PERMANENT_SESSION_LIFETIME=1800  # 30-minute timeout
```

**Session Lifecycle**:
1. User loads exam → Session created, results cleared
2. User submits → Results stored in session
3. User views results → Results retrieved from session
4. User retakes → Session cleared
5. Browser close/timeout → Session destroyed

**MVP Limitation**: No persistence across sessions (intentional)

---

## Development Workflow

### Environment Setup

#### Virtual Environment Best Practices
```bash
# Create dedicated environment per project
python3 -m venv venv

# Activate
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Verify installation
python3 -c "import flask; print(flask.__version__)"
```

#### Environment Variables
Create `.env` file (never commit to git):
```bash
# Development
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=127.0.0.1
FLASK_PORT=5000

# Secret key (generate with: python3 -c 'import secrets; print(secrets.token_hex(32))')
SECRET_KEY=your-secret-key-here

# Production (when deploying)
SESSION_COOKIE_SECURE=True
```

Load in `app.py`:
```python
from dotenv import load_dotenv
load_dotenv()

app.secret_key = os.getenv('SECRET_KEY', os.urandom(32))
```

### Development Commands

#### Running the Application
```bash
# Method 1: Direct execution
python3 app.py

# Method 2: Flask CLI (recommended)
flask --app app run --debug

# Method 3: Specify host/port
flask --app app run --host 0.0.0.0 --port 8000
```

#### Validation Commands
```bash
# Validate question structure
python3 exam_data.py

# Test grading logic
python3 grader.py

# Check Python syntax
python3 -m py_compile app.py exam_data.py grader.py
```

#### Code Quality
```bash
# Install tools
pip install flake8 black pylint

# Run linter
flake8 app.py exam_data.py grader.py

# Auto-format code
black app.py exam_data.py grader.py

# Deep analysis
pylint app.py exam_data.py grader.py
```

### Git Workflow

#### Branch Strategy
```bash
# Feature development
git checkout -b feature/add-timer-mode

# Bug fixes
git checkout -b fix/validation-error

# Documentation
git checkout -b docs/update-readme
```

#### Commit Message Convention
```
type: subject line (max 50 chars)

Body with detailed description (wrap at 72 chars)

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

#### Pull Request Process
1. Create feature branch
2. Develop and test locally
3. Run code quality checks
4. Commit with conventional messages
5. Push to remote
6. Create PR with description
7. Request review
8. Address feedback
9. Merge after approval

---

## Testing Strategy

### Manual Testing Checklist

#### Functional Testing
- [ ] All 10 questions display correctly
- [ ] Radio buttons allow single selection per question
- [ ] Form validation prevents incomplete submission
- [ ] Score calculation is accurate
- [ ] Results display correct/incorrect indicators
- [ ] Retake functionality clears session
- [ ] Flash messages display for errors

#### Cross-Browser Testing
Test on:
- Chrome (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Edge (latest 2 versions)

#### Responsive Design Testing
Breakpoints:
- Mobile: <768px
- Tablet: 768-1023px
- Desktop: ≥1024px

#### Accessibility Testing
- [ ] Keyboard navigation works (Tab, Arrow keys, Enter)
- [ ] Screen reader compatibility (NVDA, JAWS, VoiceOver)
- [ ] Color contrast meets WCAG AA (4.5:1 minimum)
- [ ] Focus indicators visible
- [ ] ARIA labels present and accurate

### Automated Testing (Future Enhancement)

#### Unit Tests (grader.py)
```python
import pytest
from grader import grade_exam, calculate_feedback_message

def test_perfect_score():
    """Test grading with all correct answers"""
    questions = {...}  # Sample questions
    user_answers = {...}  # All correct

    results = grade_exam(questions, user_answers)

    assert results['score'] == 100
    assert results['correct_count'] == 10
    assert results['percentage'] == 100.0
    assert "Outstanding" in results['feedback_message']

def test_zero_score():
    """Test grading with all incorrect answers"""
    questions = {...}
    user_answers = {...}  # All incorrect

    results = grade_exam(questions, user_answers)

    assert results['score'] == 0
    assert results['correct_count'] == 0

def test_feedback_thresholds():
    """Test feedback message accuracy"""
    assert "Outstanding" in calculate_feedback_message(95)
    assert "Excellent" in calculate_feedback_message(85)
    assert "Good job" in calculate_feedback_message(75)
```

#### Integration Tests (Flask routes)
```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test exam interface loads"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'NFL Trivia Exam' in response.data

def test_submit_validation(client):
    """Test incomplete submission validation"""
    response = client.post('/submit', data={'q1': 'A'})  # Incomplete
    assert response.status_code == 302  # Redirect
    # Check flash message appears
```

---

## Security Best Practices

### OWASP Top 10 Implementation

#### A01: Broken Access Control
**Implementation**: Session-based state management

- No URL parameters for sensitive data
- Session isolation per user
- No authentication required (MVP scope)

**Future**: User accounts with proper authorization

#### A03: Injection
**Implementation**: Three-layer input validation

```python
# Layer 1: Type checking
if not isinstance(form_data, dict):
    return False, "Invalid data type"

# Layer 2: Structure validation
if question_id not in QUESTIONS:
    return False, "Invalid question ID"

# Layer 3: Value sanitization
answer = answer.strip().upper()
if answer not in ['A', 'B', 'C', 'D']:
    return False, "Invalid answer value"
```

**Prevention**:
- No SQL injection (no database in MVP)
- Form data sanitization
- Type checking on all inputs
- Whitelist validation (A, B, C, D only)

#### A05: Security Misconfiguration
**Implementation**: Secure defaults and proper error handling

```python
# Secure session configuration
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=1800
)

# Error handling without internal exposure
@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 error: {str(error)}", exc_info=True)
    return render_template('error.html',
        error_message="An internal error occurred."
    ), 500
```

#### A07: Identification and Authentication Failures
**Implementation**: Secure session cookies

- `httponly` flag prevents XSS cookie access
- `samesite=Lax` provides CSRF protection
- 30-minute session timeout
- Secure secret key generation

#### A09: Security Logging and Monitoring Failures
**Implementation**: Comprehensive logging

```python
# Security event logging
logger.info("Exam interface loaded")
logger.warning(f"Invalid submission: {error_message}")
logger.error(f"Unexpected error: {str(e)}", exc_info=True)
```

**Logged Events**:
- Exam loads and submissions
- Validation failures
- Unexpected form fields (attack indicators)
- Error conditions

### Secret Management

**Never commit secrets to git**:
```bash
# .gitignore
.env
.env.local
*.pem
*.key
```

**Secret key generation**:
```bash
python3 -c 'import secrets; print(secrets.token_hex(32))'
```

**Environment-based configuration**:
```python
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not set")
```

---

## Performance Optimization

### Current Performance Metrics
- Page load: <2 seconds
- Grading: <500ms
- Template rendering: <100ms
- Session operations: <50ms

### Optimization Strategies

#### Caching (Future Enhancement)
```python
from flask import Flask
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@cache.cached(timeout=300, key_prefix='questions')
def get_all_questions():
    return QUESTIONS
```

#### Template Optimization
- Minimize Jinja2 logic
- Use template inheritance
- Pre-calculate values in routes
- Cache static assets with long expiry

#### Database Considerations (Future)
If adding persistence:
- Use connection pooling
- Implement query caching
- Add database indexes
- Optimize N+1 queries

---

## Troubleshooting Guide

### Common Issues

#### Issue: "ModuleNotFoundError: No module named 'flask'"
**Cause**: Virtual environment not activated or dependencies not installed

**Solution**:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

#### Issue: Port 5000 already in use
**Cause**: Another process using port 5000 (often AirPlay on macOS)

**Solution**:
```bash
# Option 1: Use different port
flask --app app run --port 8000

# Option 2: Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Option 3: Disable AirPlay (macOS)
# System Preferences → Sharing → Uncheck "AirPlay Receiver"
```

#### Issue: Session data lost on page refresh
**Cause**: Expected MVP behavior (no persistence)

**Workaround**: Complete exam in single session without refreshing

**Future Solution**: Add database persistence

#### Issue: Grading results incorrect
**Cause**: Wrong correct answer in exam_data.py

**Debug**:
```python
# Validate question structure
python3 exam_data.py

# Check specific question
from exam_data import QUESTIONS
print(QUESTIONS["q1"]["correct"])  # Should be "A", "B", "C", or "D"
```

### Debugging Techniques

#### Enable Debug Mode
```python
# app.py
if __name__ == '__main__':
    app.run(debug=True)
```

**Features**:
- Auto-reload on code changes
- Interactive debugger in browser
- Detailed error pages

**Warning**: Never use debug mode in production!

#### Logging Configuration
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

#### Flask Shell for Testing
```bash
flask --app app shell

>>> from exam_data import QUESTIONS
>>> from grader import grade_exam
>>> # Interactive testing
```

---

## Contributing Guidelines

### Code Style

Follow PEP 8:
```bash
# Maximum line length
# 79 characters for code
# 72 characters for docstrings/comments

# Indentation: 4 spaces (no tabs)

# Naming conventions
class_name = ClassName
function_name = snake_case
CONSTANT_NAME = UPPER_SNAKE_CASE
```

### Documentation Standards

Every function needs docstring:
```python
def grade_exam(questions: Dict[str, Any], user_answers: Dict[str, str]) -> Dict[str, Any]:
    """
    Grade an NFL trivia exam and provide detailed results.

    Args:
        questions: Dictionary of questions with structure defined in exam_data
        user_answers: Dictionary mapping question IDs to answer keys

    Returns:
        Results dictionary with score, feedback, and per-question details

    Raises:
        ValueError: If input validation fails
        TypeError: If inputs are not dictionaries

    Example:
        >>> results = grade_exam(QUESTIONS, {"q1": "B", "q2": "A", ...})
        >>> print(results['score'])
        80
    """
```

### Pull Request Checklist

Before submitting PR:
- [ ] Code follows PEP 8 style guidelines
- [ ] All functions have docstrings
- [ ] Manual testing completed
- [ ] No console.log() or debugging code
- [ ] Git commits follow conventional format
- [ ] README updated if needed
- [ ] Security considerations documented

---

## Next Steps

### Recommended Learning Path
1. Read PRD.md for product context
2. Review CLAUDE.md for quick reference
3. Study API_REFERENCE.md for technical details
4. Run application locally and explore code
5. Make small changes to understand data flow
6. Contribute improvements or new features

### Future Enhancement Ideas
- Add user authentication (v2.0)
- Implement database persistence
- Add question randomization
- Create timed exam mode
- Build admin dashboard
- Add analytics and reporting

---

## Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **Python Dictionary Tutorial**: https://docs.python.org/3/tutorial/datastructures.html#dictionaries
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **WCAG Guidelines**: https://www.w3.org/WAI/WCAG21/quickref/
- **PEP 8 Style Guide**: https://pep8.org/

---

**Document Version**: 1.0
**Last Updated**: November 5, 2025
**Maintained By**: Development Team
