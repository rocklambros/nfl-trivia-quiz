# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NFL Trivia Quiz is a Flask web application that tests users' NFL knowledge through a 10-question multiple-choice exam with automatic grading. The project demonstrates **dictionary-based architecture** as a core educational requirement.

**Key Characteristics**:
- MVP scope: No database, no user authentication, no score persistence
- Session-based state management (data clears on browser close)
- OWASP security implementation (input validation, session security, logging)
- WCAG 2.1 AA accessibility compliance

## Development Commands

### Running the Application
```bash
# Development mode (recommended for local testing)
python3 app.py

# Alternative: Flask CLI with auto-reload
flask --app app run --debug

# Production mode (never use debug=True in production)
flask --app app run
```

The application runs on `http://127.0.0.1:5000` by default.

### Validation and Testing
```bash
# Validate question structure
python3 exam_data.py

# Test grading logic directly
python3 grader.py

# Code style checking (if flake8 installed)
flake8 app.py exam_data.py grader.py
```

### Dependency Management
```bash
# Install dependencies
pip3 install -r requirements.txt

# Generate new requirements file (if adding dependencies)
pip3 freeze > requirements.txt
```

## Architecture Principles

### Dictionary-Based Data Flow

**CRITICAL**: This is an educational project demonstrating dictionary usage. All data structures must use Python dictionaries:

1. **Question Storage** (exam_data.py):
   ```python
   {
       "q1": {
           "question": str,
           "options": {"A": str, "B": str, "C": str, "D": str},
           "correct": str  # "A", "B", "C", or "D"
       }
   }
   ```

2. **User Responses** (captured from form):
   ```python
   {"q1": "B", "q2": "A", ...}  # 10 questions total
   ```

3. **Grading Results** (grader.py output):
   ```python
   {
       "score": int,  # 0-100
       "correct_count": int,
       "total_questions": int,
       "percentage": float,
       "feedback_message": str,
       "details": {
           "q1": {
               "user_answer": str,
               "correct_answer": str,
               "is_correct": bool
           }
       }
   }
   ```

### Three-Layer Validation Architecture

The application implements defense-in-depth with three validation layers:

1. **Client-side** (templates/index.html): HTML5 `required` attributes for immediate user feedback
2. **Application Layer** (app.py): `validate_answer_input()` checks completeness and format
3. **Business Logic** (grader.py): `validate_user_answers()` enforces data integrity

### Separation of Concerns

- **app.py**: Flask routing, session management, HTTP request/response handling, security controls
- **exam_data.py**: Question bank storage, data access methods (`get_all_questions()`, `get_question_count()`)
- **grader.py**: Pure grading logic with no I/O dependencies (testable in isolation)
- **templates/**: Jinja2 templates for presentation (index.html, results.html, error.html)
- **static/**: CSS styling only (no JavaScript frameworks in MVP)

## Security Implementation (OWASP Compliance)

### Input Validation (OWASP A03: Injection Prevention)

**Three-step validation in app.py**:
1. `validate_answer_input()`: Checks form data structure, detects unexpected fields
2. `sanitize_user_answers()`: Strips whitespace, normalizes to uppercase, validates A-D format
3. Type checking: Ensures all inputs are strings before processing

When adding new form handlers, always validate and sanitize user input before processing.

### Session Security (OWASP A07: Authentication Failures)

**Secure session configuration in app.py**:
```python
SESSION_COOKIE_HTTPONLY=True   # Prevents XSS access to cookies
SESSION_COOKIE_SAMESITE='Lax'  # CSRF protection
PERMANENT_SESSION_LIFETIME=1800  # 30-minute timeout
```

Session data is used for results storage only. Never store sensitive data in Flask sessions without encryption.

### Security Logging (OWASP A09: Logging Failures)

All security-relevant events are logged:
- Exam loads, submissions, and completions
- Invalid submissions and validation failures
- Unexpected form fields (potential attack indicators)
- Error conditions with sanitized messages

When adding new routes, include appropriate security logging.

## Adding Questions

Edit `exam_data.py` and add to the `QUESTIONS` dictionary:

```python
"q11": {
    "question": "Your question text here?",
    "options": {
        "A": "First option",
        "B": "Second option",
        "C": "Third option",
        "D": "Fourth option"
    },
    "correct": "A"
}
```

**Validation**: Run `python3 exam_data.py` to verify structure. The grading logic automatically adapts to question count changes.

## Modifying Grading Logic

Edit `grader.py` to customize:
- Score calculation algorithm (currently: percentage-based)
- Performance message thresholds (currently: 90+, 80-89, 70-79, 60-69, <60)
- Result formatting and feedback text

The grading function is pure (no side effects) and can be tested in isolation.

## Common Issues

**Port 5000 already in use**:
```bash
# Use different port
flask --app app run --port 8000

# Or set via environment variable
export FLASK_PORT=8000
python3 app.py
```

**Questions not displaying**:
- Verify `exam_data.py` structure with `python3 exam_data.py`
- Check Flask logs for template rendering errors
- Ensure `templates/index.html` exists

**Session data lost on refresh**:
- This is expected MVP behavior (no persistence)
- Users must complete exam in single session
- Future enhancement: database integration for score history

**Grading results incorrect**:
- Verify correct answers in `exam_data.py` (must be "A", "B", "C", or "D")
- Test grading logic directly: `python3 grader.py`
- Check for typos in question IDs (must match form field names)

## Environment Configuration

**Development**:
```bash
export FLASK_DEBUG=True
export FLASK_HOST=127.0.0.1
export FLASK_PORT=5000
```

**Production**:
```bash
export FLASK_ENV=production
export SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
export SESSION_COOKIE_SECURE=True
```

**NEVER commit `.env` files with `SECRET_KEY` values to version control.**

## MVP Limitations

The following are intentional MVP limitations (not bugs):
- No user accounts or authentication
- No score persistence (clears on session end)
- No question randomization
- No timed mode
- No leaderboard or social features
- Single exam category (no topic filtering)

See PRD.md section 13 for planned v2.0+ enhancements.

## Testing Strategy

**Manual testing workflow**:
1. Load exam interface → verify 10 questions display
2. Select answers → verify radio button exclusivity
3. Submit incomplete → verify validation message
4. Submit complete → verify score calculation accuracy
5. Check results → verify correct/incorrect indicators
6. Click retake → verify session cleanup

**Responsive testing**: Test at breakpoints <768px (mobile), 768-1023px (tablet), ≥1024px (desktop)

**Cross-browser**: Chrome, Firefox, Safari, Edge (latest 2 versions)

## Project Files

**Core Application**:
- `app.py` (331 lines): Flask routes, validation, session management
- `exam_data.py` (186 lines): Question bank with 10 NFL questions
- `grader.py` (279 lines): Grading algorithms and validation

**Configuration**:
- `requirements.txt`: Python dependencies (Flask 3.0.0, Werkzeug 3.0.1, Jinja2 3.1.2)
- `.gitignore`: Excludes __pycache__, venv, .env, .serena/, IDE files

**Documentation**:
- `README.md` (670 lines): Complete user and developer documentation
- `PRD.md` (525 lines): Product requirements and specifications
- `VALIDATION_REPORT.md`: Quality assurance report

**Templates** (templates/):
- `index.html`: Exam interface with form
- `results.html`: Score display and question breakdown
- `error.html`: User-friendly error pages

**Static Assets** (static/):
- `style.css`: Responsive styling with WCAG-compliant contrast

## Code Style

Follow PEP 8 conventions:
- 4 spaces for indentation (no tabs)
- Maximum line length: 79 characters (docstrings/comments), 99 for code
- Descriptive variable names (e.g., `user_answers`, not `ua`)
- Docstrings for all functions with Args/Returns sections
- Type hints for function signatures

## Git Workflow

Project is hosted at: `https://github.com/rocklambros/nfl-trivia-quiz`

**Conventional commit format**:
```
type: subject line

Body with detailed description

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

Types: feat, fix, docs, style, refactor, test, chore
