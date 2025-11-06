"""
NFL Trivia Exam - Question Bank
================================
Contains 10 NFL trivia questions covering diverse topics:
- Super Bowl history
- Team information
- Player statistics and records
- NFL rules
- League history
- Current NFL information

Structure: Python dictionary with question IDs as keys
Each question contains:
- question: str (question text)
- options: dict (A, B, C, D answer choices)
- correct: str (correct answer key)
"""

QUESTIONS = {
    "q1": {
        "question": "Which team has won the most Super Bowl championships in NFL history?",
        "options": {
            "A": "Dallas Cowboys",
            "B": "New England Patriots",
            "C": "Pittsburgh Steelers",
            "D": "San Francisco 49ers"
        },
        "correct": "B"
    },
    "q2": {
        "question": "What is the only team to complete a perfect season including winning the Super Bowl?",
        "options": {
            "A": "1972 Miami Dolphins",
            "B": "1985 Chicago Bears",
            "C": "2007 New England Patriots",
            "D": "1984 San Francisco 49ers"
        },
        "correct": "A"
    },
    "q3": {
        "question": "Which NFL team is known as 'America's Team'?",
        "options": {
            "A": "New York Giants",
            "B": "Green Bay Packers",
            "C": "Dallas Cowboys",
            "D": "New England Patriots"
        },
        "correct": "C"
    },
    "q4": {
        "question": "How many teams currently compete in the NFL?",
        "options": {
            "A": "30",
            "B": "32",
            "C": "34",
            "D": "28"
        },
        "correct": "B"
    },
    "q5": {
        "question": "Who holds the NFL record for most career touchdown passes?",
        "options": {
            "A": "Peyton Manning",
            "B": "Brett Favre",
            "C": "Tom Brady",
            "D": "Drew Brees"
        },
        "correct": "C"
    },
    "q6": {
        "question": "Which running back holds the single-season rushing record with 2,105 yards?",
        "options": {
            "A": "Barry Sanders",
            "B": "Eric Dickerson",
            "C": "Adrian Peterson",
            "D": "Derrick Henry"
        },
        "correct": "B"
    },
    "q7": {
        "question": "How many points is a safety worth in NFL football?",
        "options": {
            "A": "1 point",
            "B": "2 points",
            "C": "3 points",
            "D": "6 points"
        },
        "correct": "B"
    },
    "q8": {
        "question": "In what year was the NFL founded?",
        "options": {
            "A": "1920",
            "B": "1925",
            "C": "1933",
            "D": "1946"
        },
        "correct": "A"
    },
    "q9": {
        "question": "Which team won Super Bowl LVIII (58) in 2024?",
        "options": {
            "A": "Philadelphia Eagles",
            "B": "San Francisco 49ers",
            "C": "Kansas City Chiefs",
            "D": "Cincinnati Bengals"
        },
        "correct": "C"
    },
    "q10": {
        "question": "What is the nickname of the NFL championship trophy?",
        "options": {
            "A": "The Lombardi Trophy",
            "B": "The Halas Trophy",
            "C": "The Commissioner's Trophy",
            "D": "The Victory Cup"
        },
        "correct": "A"
    }
}


def get_all_questions():
    """
    Retrieve all questions from the question bank.

    Returns:
        dict: Dictionary containing all exam questions
    """
    return QUESTIONS


def get_question_count():
    """
    Get the total number of questions in the exam.

    Returns:
        int: Number of questions available
    """
    return len(QUESTIONS)


def validate_question_structure():
    """
    Validate that all questions follow the correct dictionary structure.

    Returns:
        tuple: (is_valid: bool, errors: list)
    """
    errors = []

    for question_id, question_data in QUESTIONS.items():
        # Check required keys
        if "question" not in question_data:
            errors.append(f"{question_id}: Missing 'question' key")
        if "options" not in question_data:
            errors.append(f"{question_id}: Missing 'options' key")
        if "correct" not in question_data:
            errors.append(f"{question_id}: Missing 'correct' key")

        # Validate options structure
        if "options" in question_data:
            options = question_data["options"]
            required_options = {"A", "B", "C", "D"}
            if set(options.keys()) != required_options:
                errors.append(f"{question_id}: Options must be exactly A, B, C, D")

        # Validate correct answer
        if "correct" in question_data:
            correct = question_data["correct"]
            if correct not in ["A", "B", "C", "D"]:
                errors.append(f"{question_id}: Correct answer must be A, B, C, or D")

    return (len(errors) == 0, errors)


# Validate questions on module load
if __name__ == "__main__":
    is_valid, errors = validate_question_structure()
    if is_valid:
        print(f"✅ All {get_question_count()} questions are valid!")
    else:
        print(f"❌ Validation errors found:")
        for error in errors:
            print(f"  - {error}")
