"""
NFL Trivia Exam Grading System

This module provides automatic grading functionality for NFL trivia exams.
Uses dictionary-based architecture for data handling and includes comprehensive
input validation and security measures.

Security measures:
- Input validation for all parameters
- Type checking for dictionaries
- Graceful handling of missing/invalid answers
- Protection against injection vulnerabilities
"""

from typing import Dict, Any, Union


def validate_questions_format(questions: Any) -> bool:
    """
    Validate that questions dictionary has the correct format.

    Args:
        questions: Questions dictionary to validate

    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(questions, dict):
        return False

    for question_id, question_data in questions.items():
        if not isinstance(question_id, str):
            return False
        if not isinstance(question_data, dict):
            return False

        required_keys = {"question", "options", "correct"}
        if not all(key in question_data for key in required_keys):
            return False

        if not isinstance(question_data["question"], str):
            return False
        if not isinstance(question_data["options"], dict):
            return False
        if not isinstance(question_data["correct"], str):
            return False

    return True


def validate_user_answers(user_answers: Any, questions: Dict[str, Any]) -> tuple[bool, str]:
    """
    Validate user answers dictionary format and completeness.

    Args:
        user_answers: User's answers dictionary
        questions: Questions dictionary for validation

    Returns:
        tuple: (is_valid, error_message)
    """
    if not isinstance(user_answers, dict):
        return False, "User answers must be a dictionary"

    # Check if all questions are answered
    expected_questions = set(questions.keys())
    provided_answers = set(user_answers.keys())

    if provided_answers != expected_questions:
        missing = expected_questions - provided_answers
        extra = provided_answers - expected_questions

        error_parts = []
        if missing:
            error_parts.append(f"Missing answers for: {', '.join(sorted(missing))}")
        if extra:
            error_parts.append(f"Unexpected answer keys: {', '.join(sorted(extra))}")

        return False, "; ".join(error_parts)

    # Validate answer types
    for question_id, answer in user_answers.items():
        if not isinstance(answer, str):
            return False, f"Answer for {question_id} must be a string"

        # Validate answer is a valid option
        valid_options = questions[question_id]["options"].keys()
        if answer not in valid_options:
            return False, f"Invalid answer '{answer}' for {question_id}. Must be one of: {', '.join(valid_options)}"

    return True, ""


def calculate_feedback_message(percentage: float) -> str:
    """
    Generate feedback message based on exam performance.

    Args:
        percentage: Score percentage (0-100)

    Returns:
        str: Appropriate feedback message
    """
    if percentage >= 90:
        return "Outstanding! You're an NFL expert!"
    elif percentage >= 80:
        return "Excellent work! Strong NFL knowledge!"
    elif percentage >= 70:
        return "Good job! Solid understanding of the NFL!"
    elif percentage >= 60:
        return "Not bad! Keep learning about the NFL!"
    else:
        return "Keep studying! Review the answers below!"


def grade_exam(questions: Dict[str, Any], user_answers: Dict[str, str]) -> Dict[str, Any]:
    """
    Grade an NFL trivia exam and provide detailed results.

    This function validates inputs, compares user answers against correct answers,
    calculates scores, and generates detailed feedback for each question.

    Args:
        questions: Dictionary of questions with format:
            {
                "q1": {
                    "question": str,
                    "options": dict,
                    "correct": str
                },
                ...
            }
        user_answers: Dictionary of user's answers with format:
            {
                "q1": "A",
                "q2": "B",
                ...
            }

    Returns:
        Dict containing:
            - score: int (0-100)
            - correct_count: int
            - total_questions: int
            - percentage: float
            - feedback_message: str
            - details: dict with per-question results

    Raises:
        ValueError: If input validation fails
        TypeError: If inputs are not dictionaries
    """
    # Validate questions format
    if not validate_questions_format(questions):
        raise ValueError(
            "Invalid questions format. Expected dictionary with structure: "
            "{question_id: {question: str, options: dict, correct: str}}"
        )

    # Validate user answers
    is_valid, error_message = validate_user_answers(user_answers, questions)
    if not is_valid:
        raise ValueError(f"Invalid user answers: {error_message}")

    # Initialize grading variables
    total_questions = len(questions)
    correct_count = 0
    details = {}

    # Grade each question
    for question_id, question_data in questions.items():
        user_answer = user_answers[question_id]
        correct_answer = question_data["correct"]
        is_correct = user_answer == correct_answer

        if is_correct:
            correct_count += 1

        details[question_id] = {
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "question_text": question_data["question"]
        }

    # Calculate scores
    percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
    score = int(percentage)

    # Generate feedback message
    feedback_message = calculate_feedback_message(percentage)

    # Construct result dictionary
    result = {
        "score": score,
        "correct_count": correct_count,
        "total_questions": total_questions,
        "percentage": round(percentage, 2),
        "feedback_message": feedback_message,
        "details": details
    }

    return result


def format_results_summary(results: Dict[str, Any]) -> str:
    """
    Format grading results into a human-readable summary.

    Args:
        results: Results dictionary from grade_exam()

    Returns:
        str: Formatted summary string
    """
    if not isinstance(results, dict):
        raise TypeError("Results must be a dictionary")

    required_keys = {"score", "correct_count", "total_questions", "feedback_message"}
    if not all(key in results for key in required_keys):
        raise ValueError("Results dictionary missing required keys")

    summary_lines = [
        "=" * 50,
        "NFL TRIVIA EXAM RESULTS",
        "=" * 50,
        f"Score: {results['score']}/100",
        f"Correct Answers: {results['correct_count']}/{results['total_questions']}",
        f"Percentage: {results['percentage']:.2f}%",
        "",
        results['feedback_message'],
        "=" * 50
    ]

    return "\n".join(summary_lines)


if __name__ == "__main__":
    # Example usage and testing
    sample_questions = {
        "q1": {
            "question": "Which team won Super Bowl LVIII?",
            "options": {
                "A": "Kansas City Chiefs",
                "B": "Philadelphia Eagles",
                "C": "San Francisco 49ers",
                "D": "Buffalo Bills"
            },
            "correct": "A"
        },
        "q2": {
            "question": "How many teams are in the NFL?",
            "options": {
                "A": "30",
                "B": "31",
                "C": "32",
                "D": "33"
            },
            "correct": "C"
        }
    }

    sample_answers = {
        "q1": "A",
        "q2": "C"
    }

    try:
        results = grade_exam(sample_questions, sample_answers)
        print(format_results_summary(results))
        print("\nDetailed Results:")
        for question_id, detail in results["details"].items():
            status = "✓" if detail["is_correct"] else "✗"
            print(f"\n{status} {question_id}: {detail['question_text']}")
            print(f"  Your answer: {detail['user_answer']}")
            print(f"  Correct answer: {detail['correct_answer']}")
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")
