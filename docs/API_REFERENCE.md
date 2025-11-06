# API Reference - NFL Trivia Quiz

**Version**: 1.0 (MVP)
**Last Updated**: November 5, 2025

## Table of Contents
- [Overview](#overview)
- [Flask Routes](#flask-routes)
- [Core Modules](#core-modules)
  - [exam_data.py](#exam_datapy)
  - [grader.py](#graderpy)
  - [app.py](#apppy)
- [Data Structures](#data-structures)
- [Security Functions](#security-functions)
- [Error Handling](#error-handling)

---

## Overview

The NFL Trivia Quiz API consists of Flask HTTP routes and three core Python modules. All data structures use Python dictionaries as per the educational architecture requirement.

**Technology Stack**:
- Flask 3.0.0 (Web framework)
- Python 3.8+ (Backend language)
- Jinja2 3.1.2 (Template engine)

---

## Flask Routes

### `GET /`
**Display Exam Interface**

Renders the exam interface with all 10 questions.

**Request**: None
**Response**: HTML page with exam form

**Session Management**:
- Clears any existing results from session
- Initializes fresh exam state

**Template Variables**:
```python
{
    "questions": dict,        # All questions from exam_data.QUESTIONS
    "total_questions": int    # Question count (10)
}
```

**Error Handling**:
- Returns 500 error page if questions cannot be loaded
- Logs error details without exposing internals

**Example**:
```bash
curl http://localhost:5000/
```

---

### `POST /submit`
**Process Exam Submission**

Validates answers, grades exam, and stores results in session.

**Request**: Form data with question answers

**Form Parameters**:
```
q1=A&q2=B&q3=C&q4=D&q5=A&q6=B&q7=B&q8=A&q9=C&q10=A
```

**Validation Layers**:
1. `validate_answer_input()` - Structure and completeness
2. `sanitize_user_answers()` - Format normalization
3. Final completeness check

**Response**: Redirect to `/results`

**Session Storage**:
```python
session['results'] = {
    "score": int,              # 0-100
    "correct_count": int,      # Number correct
    "total_questions": int,    # Total (10)
    "percentage": float,       # Score percentage
    "feedback_message": str,   # Performance message
    "details": dict           # Question-by-question breakdown
}
```

**Error Conditions**:
- Missing answers → Flash message + redirect to `/`
- Invalid answer format → Flash message + redirect to `/`
- Grading failure → Error page with user-friendly message

**Security**:
- OWASP A03 (Injection): Input validation and sanitization
- OWASP A07 (Session): Secure session storage
- OWASP A09 (Logging): Security event logging

**Example**:
```bash
curl -X POST http://localhost:5000/submit \
  -d "q1=B&q2=A&q3=C&q4=B&q5=C&q6=B&q7=B&q8=A&q9=C&q10=A"
```

---

### `GET /results`
**Display Grading Results**

Shows score and question-by-question breakdown from session.

**Request**: None (reads from session)
**Response**: HTML page with results

**Template Variables**:
```python
{
    "results": dict,          # From session
    "questions": dict         # For answer text lookup
}
```

**Access Control**:
- Redirects to `/` if no results in session
- Flash message prompts user to complete exam

**Error Handling**:
- Validates results structure (defense in depth)
- Redirects to `/` on invalid session data

**Example**:
```bash
curl http://localhost:5000/results \
  --cookie "session=..."
```

---

### `GET /retake`
**Clear Session and Restart Exam**

Clears all session data and redirects to fresh exam.

**Request**: None
**Response**: Redirect to `/`

**Session Management**:
- Calls `session.clear()` to remove all data
- Logs retake event

**Example**:
```bash
curl http://localhost:5000/retake
```

---

## Core Modules

### exam_data.py

**Purpose**: Question bank storage and access methods

#### Constants

##### `QUESTIONS`
**Type**: `Dict[str, Dict[str, Any]]`

Dictionary of 10 NFL trivia questions.

**Structure**:
```python
{
    "q1": {
        "question": str,         # Question text
        "options": {
            "A": str,            # Option A text
            "B": str,            # Option B text
            "C": str,            # Option C text
            "D": str             # Option D text
        },
        "correct": str           # Correct answer ("A", "B", "C", or "D")
    },
    # ... q2 through q10
}
```

**Example**:
```python
from exam_data import QUESTIONS

# Access question 1
q1 = QUESTIONS["q1"]
print(q1["question"])  # "Which team has won the most Super Bowl championships?"
print(q1["correct"])   # "B"
```

---

#### Functions

##### `get_all_questions()`
**Returns all questions from the question bank**

**Parameters**: None

**Returns**: `Dict[str, Dict[str, Any]]`
Complete QUESTIONS dictionary

**Example**:
```python
from exam_data import get_all_questions

questions = get_all_questions()
# Returns full QUESTIONS dictionary
```

---

##### `get_question_count()`
**Returns the total number of questions**

**Parameters**: None

**Returns**: `int`
Number of questions (always 10 in MVP)

**Example**:
```python
from exam_data import get_question_count

count = get_question_count()
print(count)  # 10
```

---

##### `validate_question_structure()`
**Validates all questions follow correct format**

Checks for required keys, validates options structure, and verifies correct answer format.

**Parameters**: None

**Returns**: `Tuple[bool, List[str]]`
- `bool`: True if all valid, False otherwise
- `List[str]`: List of error messages (empty if valid)

**Validation Rules**:
- Each question must have `question`, `options`, `correct` keys
- Options must have exactly A, B, C, D keys
- Correct answer must be "A", "B", "C", or "D"

**Example**:
```python
from exam_data import validate_question_structure

is_valid, errors = validate_question_structure()
if is_valid:
    print("All questions valid!")
else:
    for error in errors:
        print(f"Error: {error}")
```

---

### grader.py

**Purpose**: Automatic grading logic and score calculation

#### Functions

##### `grade_exam(questions, user_answers)`
**Grades an NFL trivia exam and returns detailed results**

Main grading function with comprehensive validation and scoring.

**Parameters**:
- `questions` (`Dict[str, Any]`): Questions dictionary from exam_data
- `user_answers` (`Dict[str, str]`): User's answers
  ```python
  {"q1": "B", "q2": "A", ..., "q10": "A"}
  ```

**Returns**: `Dict[str, Any]`
```python
{
    "score": int,              # 0-100
    "correct_count": int,      # Number of correct answers
    "total_questions": int,    # Total questions (10)
    "percentage": float,       # Score percentage (rounded to 2 decimals)
    "feedback_message": str,   # Performance feedback
    "details": {
        "q1": {
            "user_answer": str,      # User's answer
            "correct_answer": str,   # Correct answer
            "is_correct": bool,      # Whether answer was correct
            "question_text": str     # Question text for reference
        },
        # ... for all questions
    }
}
```

**Raises**:
- `ValueError`: Invalid question format or user answer validation failure
- `TypeError`: Non-dictionary inputs

**Validation Steps**:
1. Question format validation via `validate_questions_format()`
2. User answer validation via `validate_user_answers()`
3. Type checking on all inputs

**Example**:
```python
from exam_data import QUESTIONS
from grader import grade_exam

user_answers = {
    "q1": "B", "q2": "A", "q3": "C", "q4": "B", "q5": "C",
    "q6": "B", "q7": "B", "q8": "A", "q9": "C", "q10": "A"
}

results = grade_exam(QUESTIONS, user_answers)
print(f"Score: {results['score']}/100")
print(f"Feedback: {results['feedback_message']}")
```

---

##### `validate_questions_format(questions)`
**Validates question dictionary structure**

**Parameters**:
- `questions` (`Any`): Questions dictionary to validate

**Returns**: `bool`
True if valid structure, False otherwise

**Validation Rules**:
- Must be dict type
- All keys must be strings
- All values must be dicts with required keys
- Required keys: `question`, `options`, `correct`

**Example**:
```python
from grader import validate_questions_format

is_valid = validate_questions_format(QUESTIONS)
# Returns True if structure is correct
```

---

##### `validate_user_answers(user_answers, questions)`
**Validates user answers completeness and format**

**Parameters**:
- `user_answers` (`Any`): User's answers to validate
- `questions` (`Dict[str, Any]`): Questions for reference

**Returns**: `Tuple[bool, str]`
- `bool`: True if valid, False otherwise
- `str`: Error message (empty string if valid)

**Validation Rules**:
- Must be dict type
- All question IDs must be answered
- No extra answer keys allowed
- All answers must be strings
- All answers must be valid options (A, B, C, or D)

**Example**:
```python
from grader import validate_user_answers

user_answers = {"q1": "B", "q2": "A", ..., "q10": "A"}
is_valid, error_msg = validate_user_answers(user_answers, QUESTIONS)

if not is_valid:
    print(f"Validation error: {error_msg}")
```

---

##### `calculate_feedback_message(percentage)`
**Generates performance feedback based on score**

**Parameters**:
- `percentage` (`float`): Score percentage (0-100)

**Returns**: `str`
Appropriate feedback message

**Feedback Thresholds**:
- 90-100%: "Outstanding! You're an NFL expert!"
- 80-89%: "Excellent work! Strong NFL knowledge!"
- 70-79%: "Good job! Solid understanding of the NFL!"
- 60-69%: "Not bad! Keep learning about the NFL!"
- Below 60%: "Keep studying! Review the answers below!"

**Example**:
```python
from grader import calculate_feedback_message

message = calculate_feedback_message(85.5)
print(message)  # "Excellent work! Strong NFL knowledge!"
```

---

##### `format_results_summary(results)`
**Formats grading results into human-readable text**

**Parameters**:
- `results` (`Dict[str, Any]`): Results dictionary from `grade_exam()`

**Returns**: `str`
Formatted summary text with borders and line breaks

**Raises**:
- `TypeError`: If results is not a dictionary
- `ValueError`: If required keys are missing

**Example**:
```python
from grader import format_results_summary

results = grade_exam(QUESTIONS, user_answers)
summary = format_results_summary(results)
print(summary)
```

**Output**:
```
==================================================
NFL TRIVIA EXAM RESULTS
==================================================
Score: 80/100
Correct Answers: 8/10
Percentage: 80.00%

Excellent work! Strong NFL knowledge!
==================================================
```

---

### app.py

**Purpose**: Flask application with routing and security

#### Security Functions

##### `validate_answer_input(form_data)`
**Validates user input from form submission**

**Security**: OWASP A03 (Injection Prevention)

**Parameters**:
- `form_data` (`Dict[str, Any]`): Form data from request

**Returns**: `Tuple[bool, str]`
- `bool`: True if valid, False otherwise
- `str`: Error message (empty if valid)

**Validation Checks**:
1. Form data exists and is not empty
2. No unexpected form fields (injection detection)
3. All required questions answered
4. Answer values are valid (A, B, C, or D)
5. Type validation (all answers must be strings)

**Example**:
```python
from app import validate_answer_input

is_valid, error = validate_answer_input(request.form)
if not is_valid:
    flash(error, 'error')
```

---

##### `sanitize_user_answers(form_data)`
**Sanitizes and normalizes user answers**

**Security**: OWASP A03 (Injection Prevention)

**Parameters**:
- `form_data` (`Dict[str, Any]`): Raw form data

**Returns**: `Dict[str, str]`
Sanitized answers dictionary with only valid question IDs

**Sanitization Steps**:
1. Removes non-question fields (CSRF tokens, etc.)
2. Strips whitespace from answers
3. Converts to uppercase
4. Validates single character A-D format
5. Rejects any answer not matching pattern

**Example**:
```python
from app import sanitize_user_answers

sanitized = sanitize_user_answers(request.form)
# Returns clean dictionary: {"q1": "A", "q2": "B", ...}
```

---

#### Configuration

##### Session Security Settings
```python
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', os.urandom(32)),
    SESSION_COOKIE_SECURE=os.environ.get('SESSION_COOKIE_SECURE', 'False') == 'True',
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=1800  # 30 minutes
)
```

**Security Features**:
- `SESSION_COOKIE_HTTPONLY`: Prevents XSS access to cookies
- `SESSION_COOKIE_SAMESITE`: CSRF protection
- `PERMANENT_SESSION_LIFETIME`: Auto-expire sessions
- `SESSION_COOKIE_SECURE`: HTTPS-only (production)

---

## Data Structures

### Question Dictionary
```python
{
    "question_id": {
        "question": "Question text?",
        "options": {
            "A": "First option",
            "B": "Second option",
            "C": "Third option",
            "D": "Fourth option"
        },
        "correct": "A"  # or "B", "C", "D"
    }
}
```

### User Answers Dictionary
```python
{
    "q1": "A",
    "q2": "B",
    "q3": "C",
    # ... all 10 questions
}
```

### Results Dictionary
```python
{
    "score": 80,                  # Integer 0-100
    "correct_count": 8,           # Number correct
    "total_questions": 10,        # Total questions
    "percentage": 80.0,           # Float with 2 decimals
    "feedback_message": "Excellent work!",
    "details": {
        "q1": {
            "user_answer": "B",
            "correct_answer": "B",
            "is_correct": True,
            "question_text": "Which team..."
        }
        # ... for all questions
    }
}
```

---

## Security Functions

### Input Validation
All user input undergoes three-layer validation:
1. **Client-side**: HTML5 `required` attributes
2. **Application**: `validate_answer_input()` function
3. **Business logic**: `validate_user_answers()` in grader

### Session Management
- Secure cookies with `httponly` and `samesite` flags
- 30-minute timeout for automatic cleanup
- Session data cleared on retake

### Logging
Security events logged:
- Exam loads and completions
- Invalid submissions
- Unexpected form fields (attack indicators)
- Error conditions

---

## Error Handling

### HTTP Error Handlers

#### `404 Not Found`
Returns user-friendly error page with navigation link.

#### `500 Internal Server Error`
Returns generic error page without exposing internals (OWASP A05).

### Exception Handling

#### `ValueError`
Raised for validation failures in grading logic.

#### `TypeError`
Raised for incorrect data types in function parameters.

### Error Responses

All errors return:
- User-friendly message (no stack traces)
- Redirect to safe page (exam homepage)
- Flash message for context
- Detailed logging (server-side only)

---

## Usage Examples

### Complete Exam Flow
```python
from flask import Flask, session
from exam_data import QUESTIONS
from grader import grade_exam

# 1. Display exam
questions = get_all_questions()

# 2. User submits answers
user_answers = {
    "q1": "B", "q2": "A", "q3": "C", "q4": "B", "q5": "C",
    "q6": "B", "q7": "B", "q8": "A", "q9": "C", "q10": "A"
}

# 3. Validate and sanitize
is_valid, error = validate_answer_input(user_answers)
if not is_valid:
    return redirect(url_for('index'))

sanitized = sanitize_user_answers(user_answers)

# 4. Grade exam
results = grade_exam(QUESTIONS, sanitized)

# 5. Store in session
session['results'] = results

# 6. Display results
# Template receives results and questions
```

### Adding New Questions
```python
from exam_data import QUESTIONS, validate_question_structure

# Add new question
QUESTIONS["q11"] = {
    "question": "Who won Super Bowl LIX?",
    "options": {
        "A": "Team A",
        "B": "Team B",
        "C": "Team C",
        "D": "Team D"
    },
    "correct": "A"
}

# Validate structure
is_valid, errors = validate_question_structure()
if not is_valid:
    print("Validation errors:", errors)
```

---

## API Changelog

### Version 1.0 (MVP) - November 5, 2025
- Initial release
- 10 NFL trivia questions
- Automatic grading functionality
- Session-based state management
- OWASP security implementation
- WCAG 2.1 AA accessibility

---

## Support

For issues or questions:
- **GitHub**: https://github.com/rocklambros/nfl-trivia-quiz
- **Documentation**: See README.md and PRD.md

---

**Last Updated**: November 5, 2025
**API Version**: 1.0 (MVP)
