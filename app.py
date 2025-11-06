"""
NFL Trivia Exam - Flask Application
====================================
Web application for administering and grading NFL trivia exams.

Security Features:
- OWASP A01 (Access Control): Session-based state management
- OWASP A03 (Injection): Input validation and sanitization
- OWASP A05 (Security Misconfiguration): Secure session configuration
- OWASP A07 (Authentication): Secure session cookies with httponly/samesite
- OWASP A09 (Logging): Security event logging for submissions

Routes:
- GET /: Display exam interface with questions
- POST /submit: Process answers, grade exam, store results
- GET /results: Display grading results
- GET /retake: Clear session and restart exam
"""

import os
import logging
from typing import Dict, Any
from flask import Flask, render_template, request, redirect, url_for, session, flash
from exam_data import QUESTIONS, get_all_questions, get_question_count
from grader import grade_exam


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask application
app = Flask(__name__)

# Security configuration - OWASP A05 & A07 compliance
app.config.update(
    # Generate secure secret key for production
    SECRET_KEY=os.environ.get('SECRET_KEY', os.urandom(32)),

    # Session security settings
    SESSION_COOKIE_SECURE=os.environ.get('SESSION_COOKIE_SECURE', 'False') == 'True',
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=1800,  # 30 minutes

    # Additional security headers
    SEND_FILE_MAX_AGE_DEFAULT=300,
)


def validate_answer_input(form_data: Dict[str, Any]) -> tuple[bool, str]:
    """
    Validate user input from form submission.

    Security: OWASP A03 (Injection Prevention)
    - Validates data types
    - Checks for required fields
    - Sanitizes input values

    Args:
        form_data: Form data from request

    Returns:
        tuple: (is_valid, error_message)
    """
    if not form_data:
        return False, "No answers submitted"

    # Check for unexpected form fields (potential injection)
    expected_keys = set(QUESTIONS.keys())
    provided_keys = set(form_data.keys())

    # Allow CSRF token and other framework fields
    unexpected_keys = provided_keys - expected_keys
    if unexpected_keys and not all(k.startswith('csrf') for k in unexpected_keys):
        logger.warning(f"Unexpected form fields detected: {unexpected_keys}")
        return False, "Invalid form data"

    # Validate all required questions are answered
    missing_questions = expected_keys - provided_keys
    if missing_questions:
        missing_list = sorted(missing_questions)
        return False, f"Please answer all questions. Missing: {', '.join(missing_list)}"

    # Validate answer values are valid options
    for question_id, answer in form_data.items():
        if question_id not in QUESTIONS:
            continue  # Skip CSRF tokens

        # Type validation
        if not isinstance(answer, str):
            return False, f"Invalid answer type for {question_id}"

        # Value sanitization - only allow A, B, C, D
        answer_upper = answer.strip().upper()
        if answer_upper not in ['A', 'B', 'C', 'D']:
            logger.warning(f"Invalid answer value detected: {answer} for {question_id}")
            return False, f"Invalid answer for {question_id}"

    return True, ""


def sanitize_user_answers(form_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Sanitize and normalize user answers from form submission.

    Security: OWASP A03 (Injection Prevention)
    - Removes non-question fields
    - Normalizes answer format
    - Validates against expected structure

    Args:
        form_data: Raw form data from request

    Returns:
        dict: Sanitized answers dictionary
    """
    sanitized = {}

    for question_id in QUESTIONS.keys():
        if question_id in form_data:
            # Sanitize: strip whitespace, convert to uppercase
            answer = form_data[question_id].strip().upper()

            # Additional validation: must be single character A-D
            if len(answer) == 1 and answer in ['A', 'B', 'C', 'D']:
                sanitized[question_id] = answer

    return sanitized


@app.route('/')
def index():
    """
    Display exam interface with all questions.

    Security:
    - Clear any existing session data on fresh exam load
    - No user data exposure

    Returns:
        Rendered exam template with questions
    """
    try:
        # Clear previous session data for fresh exam
        session.pop('results', None)

        # Load questions
        questions = get_all_questions()
        total_questions = get_question_count()

        logger.info("Exam interface loaded")

        return render_template(
            'index.html',
            questions=questions,
            total_questions=total_questions
        )
    except Exception as e:
        logger.error(f"Error loading exam interface: {str(e)}")
        return render_template(
            'error.html',
            error_message="Unable to load exam. Please try again later."
        ), 500


@app.route('/submit', methods=['POST'])
def submit():
    """
    Process exam submission, grade answers, and redirect to results.

    Security: OWASP A03, A07, A09 compliance
    - Input validation and sanitization
    - Secure session storage
    - Security event logging
    - No direct user input in responses

    Returns:
        Redirect to results page or back to exam with errors
    """
    try:
        # Validate request data
        is_valid, error_message = validate_answer_input(request.form)
        if not is_valid:
            logger.warning(f"Invalid submission: {error_message}")
            flash(error_message, 'error')
            return redirect(url_for('index'))

        # Sanitize user answers
        user_answers = sanitize_user_answers(request.form)

        # Validate completeness after sanitization
        if len(user_answers) != get_question_count():
            logger.warning(
                f"Incomplete answers after sanitization: {len(user_answers)}/{get_question_count()}"
            )
            flash("Please answer all questions with valid options (A, B, C, or D)", 'error')
            return redirect(url_for('index'))

        # Grade the exam
        results = grade_exam(QUESTIONS, user_answers)

        # Store results in session (OWASP A07: Secure session management)
        session['results'] = results
        session.modified = True

        # Log successful submission (OWASP A09: Security logging)
        logger.info(
            f"Exam graded - Score: {results['score']}/100, "
            f"Correct: {results['correct_count']}/{results['total_questions']}"
        )

        return redirect(url_for('results'))

    except ValueError as e:
        # Handle grading validation errors
        logger.error(f"Grading validation error: {str(e)}")
        flash("Invalid exam submission. Please check your answers and try again.", 'error')
        return redirect(url_for('index'))

    except Exception as e:
        # Handle unexpected errors without exposing internals (OWASP A05)
        logger.error(f"Unexpected error during submission: {str(e)}", exc_info=True)
        flash("An error occurred while processing your exam. Please try again.", 'error')
        return redirect(url_for('index'))


@app.route('/results')
def results():
    """
    Display grading results from session storage.

    Security:
    - Session-based data retrieval (no URL parameters)
    - Validates session data exists
    - No direct user input display

    Returns:
        Rendered results template or redirect to exam if no results
    """
    try:
        # Retrieve results from session
        exam_results = session.get('results')

        if not exam_results:
            logger.warning("Results page accessed without exam completion")
            flash("Please complete the exam first.", 'info')
            return redirect(url_for('index'))

        # Validate results structure (defense in depth)
        required_keys = {'score', 'correct_count', 'total_questions', 'feedback_message', 'details'}
        if not all(key in exam_results for key in required_keys):
            logger.error("Invalid results structure in session")
            flash("Invalid results data. Please retake the exam.", 'error')
            return redirect(url_for('index'))

        logger.info("Results page displayed")

        return render_template(
            'results.html',
            results=exam_results,
            questions=QUESTIONS
        )

    except Exception as e:
        logger.error(f"Error displaying results: {str(e)}", exc_info=True)
        flash("Unable to display results. Please retake the exam.", 'error')
        return redirect(url_for('index'))


@app.route('/retake')
def retake():
    """
    Clear session data and restart exam.

    Security:
    - Proper session cleanup
    - No data persistence

    Returns:
        Redirect to exam homepage
    """
    try:
        # Clear session data
        session.clear()
        logger.info("Session cleared for exam retake")

        return redirect(url_for('index'))

    except Exception as e:
        logger.error(f"Error during retake: {str(e)}")
        return redirect(url_for('index'))


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors with user-friendly message."""
    logger.warning(f"404 error: {request.url}")
    return render_template(
        'error.html',
        error_message="Page not found. Return to the exam homepage."
    ), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors without exposing internals."""
    logger.error(f"500 error: {str(error)}", exc_info=True)
    return render_template(
        'error.html',
        error_message="An internal error occurred. Please try again later."
    ), 500


if __name__ == '__main__':
    # Development server configuration
    # For production: use WSGI server (gunicorn, uWSGI)
    debug_mode = os.environ.get('FLASK_DEBUG', 'False') == 'True'

    if debug_mode:
        logger.warning("Running in DEBUG mode - NOT for production!")

    app.run(
        host=os.environ.get('FLASK_HOST', '127.0.0.1'),
        port=int(os.environ.get('FLASK_PORT', 5000)),
        debug=debug_mode
    )
