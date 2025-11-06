# NFL Trivia Exam

A web-based educational assessment tool that tests users' knowledge of National Football League history, rules, teams, and players through a 10-question multiple-choice format with automatic grading capabilities.

## Features

- **10 NFL Trivia Questions**: Diverse topics covering Super Bowl history, teams, players, rules, and league information
- **Multiple-Choice Format**: Four answer options (A, B, C, D) for each question
- **Automatic Grading**: Instant score calculation with detailed feedback
- **Immediate Results**: See your performance immediately after submission
- **Score Breakdown**: Question-by-question analysis showing correct answers and your responses
- **Performance Feedback**: Contextual messages based on your score
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Accessibility**: Semantic HTML, keyboard navigation, and screen reader support
- **Retake Capability**: Practice unlimited times to improve your NFL knowledge

## Tech Stack

- **Backend**: Python 3.8+ with Flask 3.0 web framework
- **Frontend**: HTML5, CSS3, vanilla JavaScript
- **Architecture**: Dictionary-based data structures
- **Template Engine**: Jinja2 (Flask default)
- **Session Management**: Flask sessions for temporary state

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher**: [Download Python](https://www.python.org/downloads/)
- **pip**: Python package installer (included with Python 3.8+)
- **Modern web browser**: Chrome, Firefox, Safari, or Edge (latest 2 versions)

## Installation

### Step 1: Clone or Download the Project

**Option A: Clone with Git**
```bash
git clone <repository-url>
cd nfl-trivia-exam
```

**Option B: Download ZIP**
1. Download the project ZIP file
2. Extract to your desired location
3. Navigate to the project directory

### Step 2: Create Virtual Environment (Recommended)

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask 3.0.0 (web framework)
- Werkzeug 3.0.1 (WSGI utilities)
- Jinja2 3.1.2 (template engine)
- MarkupSafe 2.1.1 (safe string handling)

### Step 4: Verify Installation

```bash
python exam_data.py
```

Expected output: `✅ All 10 questions are valid!`

## Usage

### Running the Application

**Development Mode (Recommended for Testing):**
```bash
flask --app app run --debug
```

**Alternative Method:**
```bash
python app.py
```

**Production Mode:**
```bash
flask --app app run
```

### Accessing the Exam

1. Open your web browser
2. Navigate to: `http://localhost:5000`
3. The exam interface will load with 10 questions

### Taking the Exam

1. **Read each question carefully** - 10 multiple-choice questions covering various NFL topics
2. **Select your answer** - Click the radio button next to your chosen option (A, B, C, or D)
3. **Review your selections** - Ensure all questions are answered
4. **Submit** - Click the "Submit Exam" button at the bottom of the page
5. **View results** - Your score and detailed feedback appear immediately

### Understanding Your Results

The results page displays:
- **Overall Score**: Percentage and fraction (e.g., "8/10 - 80%")
- **Performance Message**: Contextual feedback based on your score
  - 90-100%: "Outstanding! You're an NFL expert!"
  - 80-89%: "Excellent work! Strong NFL knowledge!"
  - 70-79%: "Good job! Solid understanding of the NFL!"
  - 60-69%: "Not bad! Keep learning about the NFL!"
  - Below 60%: "Keep studying! Review the answers below!"
- **Question Breakdown**: Your answer vs. correct answer for each question
- **Visual Indicators**: Checkmarks for correct answers, X marks for incorrect

### Retaking the Exam

Click the "Retake Exam" button on the results page to start fresh with a new attempt.

## Project Structure

```
nfl-trivia-exam/
├── app.py                 # Flask application with routing logic
├── exam_data.py           # Question bank (dictionary structure)
├── grader.py              # Grading logic and score calculation
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── PRD.md                 # Product requirements document
├── templates/             # HTML templates
│   ├── index.html         # Exam interface
│   ├── results.html       # Results display
│   └── error.html         # Error handling page
└── static/                # Static assets
    └── style.css          # Responsive styling
```

### Component Descriptions

**app.py**
- Flask application initialization
- Route definitions (`/`, `/submit`)
- Request handling and response logic
- Session management
- Error handling

**exam_data.py**
- Question bank storage using Python dictionaries
- 10 NFL trivia questions with correct answers
- Question validation functions
- Data access methods (`get_all_questions()`, `get_question_count()`)

**grader.py**
- Score calculation algorithm
- Answer comparison logic
- Results dictionary generation
- Performance message determination

**templates/index.html**
- Exam presentation interface
- Form structure with radio button inputs
- Question numbering and formatting
- Submit button with validation

**templates/results.html**
- Score display
- Performance feedback message
- Question-by-question breakdown
- Retake exam functionality

**templates/error.html**
- Error message display
- User-friendly error handling
- Navigation back to exam

**static/style.css**
- Responsive layout styles
- Mobile-first design approach
- Accessibility enhancements
- Visual feedback for user interactions

## Architecture Overview

### Data Flow

```
User Request → Flask Route → Exam Data → HTML Template → User Browser
                                ↓
                         Form Submission
                                ↓
                    Flask /submit Route → Grader Logic
                                ↓
                    Results Dictionary → Results Template → User Browser
```

### Dictionary-Based Architecture

The application uses Python dictionaries for all data structures:

**Question Structure:**
```python
{
    "q1": {
        "question": "Which team has won the most Super Bowl championships?",
        "options": {
            "A": "Dallas Cowboys",
            "B": "New England Patriots",
            "C": "Pittsburgh Steelers",
            "D": "San Francisco 49ers"
        },
        "correct": "B"
    }
}
```

**User Response Structure:**
```python
{
    "q1": "B",
    "q2": "A",
    "q3": "C",
    # ... all 10 questions
}
```

**Grading Results Structure:**
```python
{
    "score": 80,
    "correct_count": 8,
    "total_questions": 10,
    "percentage": 80.0,
    "feedback_message": "Excellent work! Strong NFL knowledge!",
    "details": {
        "q1": {
            "user_answer": "B",
            "correct_answer": "B",
            "is_correct": True
        }
    }
}
```

### Session Management

- **Flask Sessions**: Temporary state storage during browser session
- **Session Isolation**: Each user has independent session data
- **No Persistence**: Scores are not saved between sessions (MVP limitation)
- **Security**: Session data cleared on browser close

## Development Guide

### Adding New Questions

Edit `exam_data.py` and add questions to the `QUESTIONS` dictionary:

```python
"q11": {
    "question": "Your question text here?",
    "options": {
        "A": "First option",
        "B": "Second option",
        "C": "Third option",
        "D": "Fourth option"
    },
    "correct": "A"  # Correct answer key
}
```

**Validation:**
```bash
python exam_data.py
```

### Modifying Grading Logic

Edit `grader.py` to customize:
- Score calculation algorithm
- Performance message thresholds
- Result formatting
- Feedback messages

Example customization:
```python
# Change performance message thresholds
if percentage >= 95:
    return "Perfect score! NFL Hall of Fame knowledge!"
elif percentage >= 85:
    return "Outstanding work! You're a true fan!"
```

### Customizing Styling

Edit `static/style.css` to modify:
- Color scheme
- Typography
- Layout spacing
- Responsive breakpoints
- Button styles

**Responsive Breakpoints:**
- Desktop: ≥1024px
- Tablet: 768-1023px
- Mobile: <768px

### Running in Debug Mode

Debug mode provides:
- Automatic reloading on code changes
- Detailed error messages
- Interactive debugger

```bash
flask --app app run --debug
```

**Warning:** Never use debug mode in production!

### Code Style Guidelines

This project follows PEP 8 Python style guidelines:
- 4 spaces for indentation
- Maximum line length: 79 characters
- Descriptive variable and function names
- Docstrings for all functions
- Clear separation of concerns

**Check code style:**
```bash
# Install flake8
pip install flake8

# Run linting
flake8 app.py exam_data.py grader.py
```

## Testing

### Manual Testing Steps

**1. Test Question Display**
- Load `http://localhost:5000`
- Verify all 10 questions appear
- Check that 4 options (A, B, C, D) display for each question
- Confirm radio buttons are selectable

**2. Test Answer Selection**
- Select an answer for each question
- Verify only one option can be selected per question
- Try changing selections to ensure updates work

**3. Test Incomplete Submission**
- Leave questions unanswered
- Click "Submit Exam"
- Verify appropriate validation message appears

**4. Test Grading Accuracy**
- Answer all questions with known correct answers
- Submit the exam
- Verify score calculation is correct
- Check that correct answers are properly highlighted

**5. Test Results Display**
- Verify score displays in both percentage and fraction format
- Confirm performance message matches score
- Check that all 10 questions appear in breakdown
- Verify correct vs incorrect indicators display properly

**6. Test Retake Functionality**
- Click "Retake Exam" button
- Verify return to fresh exam with no previous answers
- Complete another attempt to test isolation

**7. Test Responsive Design**
- Resize browser window to mobile width (<768px)
- Test on tablet size (768-1023px)
- Verify layout adapts appropriately
- Check touch targets are adequate size

### Automated Testing (Future Enhancement)

Example test cases for grading logic:

```python
# Test perfect score
def test_perfect_score():
    user_answers = {
        "q1": "B", "q2": "A", "q3": "C", "q4": "B", "q5": "C",
        "q6": "B", "q7": "B", "q8": "A", "q9": "C", "q10": "A"
    }
    results = grade_exam(QUESTIONS, user_answers)
    assert results["score"] == 100
    assert results["correct_count"] == 10

# Test zero score
def test_zero_score():
    user_answers = {f"q{i}": "D" if QUESTIONS[f"q{i}"]["correct"] != "D" else "A"
                    for i in range(1, 11)}
    results = grade_exam(QUESTIONS, user_answers)
    assert results["score"] == 0
```

## Deployment

### Production Considerations

**Environment Variables**

Create a `.env` file for production settings:
```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
```

**Generate Secret Key:**
```python
python -c 'import secrets; print(secrets.token_hex(32))'
```

**Load Environment Variables in app.py:**
```python
from dotenv import load_dotenv
load_dotenv()

app.secret_key = os.getenv('SECRET_KEY', 'fallback-dev-key')
```

### WSGI Server Deployment

**Option 1: Gunicorn (Recommended)**
```bash
# Install Gunicorn
pip install gunicorn

# Run with 4 worker processes
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

**Option 2: uWSGI**
```bash
# Install uWSGI
pip install uwsgi

# Run with configuration
uwsgi --http :8000 --wsgi-file app.py --callable app --processes 4
```

### Security Hardening for Production

**1. Enable HTTPS**
- Use SSL/TLS certificates (Let's Encrypt recommended)
- Redirect HTTP to HTTPS
- Set secure cookie flags

**2. Configure Security Headers**
```python
from flask import Flask

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

**3. Input Validation**
- Already implemented in form processing
- Verify all user inputs are sanitized
- Use Flask's built-in request validation

**4. Rate Limiting** (Future Enhancement)
```bash
pip install flask-limiter
```

**5. Disable Debug Mode**
```python
if __name__ == '__main__':
    app.run(debug=False)
```

## Troubleshooting

### Common Issues and Solutions

**Issue: Flask command not found**
```
Solution: Ensure virtual environment is activated
- macOS/Linux: source venv/bin/activate
- Windows: venv\Scripts\activate
```

**Issue: Port 5000 already in use**
```
Solution: Use a different port
flask --app app run --port 8000
```

**Issue: Questions not displaying**
```
Solution: Verify exam_data.py structure
python exam_data.py
```

**Issue: Session data lost on refresh**
```
Solution: This is expected MVP behavior. Future versions will implement persistence.
Current workaround: Complete exam in single session without refreshing.
```

**Issue: Styling not loading**
```
Solution: Clear browser cache or force reload
- Chrome/Firefox: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
- Verify static/style.css exists
```

**Issue: Grading results incorrect**
```
Solution: Check answer key in exam_data.py
Verify correct answer format (must be "A", "B", "C", or "D")
```

### Debug Tips

**Enable verbose error messages:**
```python
# In app.py
app.config['PROPAGATE_EXCEPTIONS'] = True
```

**Check Flask logs:**
```bash
flask --app app run --debug
```

**Validate question structure:**
```python
from exam_data import validate_question_structure
is_valid, errors = validate_question_structure()
print(errors)
```

**Test grading logic directly:**
```python
from grader import grade_exam
from exam_data import QUESTIONS

test_answers = {"q1": "B", "q2": "A", ...}
results = grade_exam(QUESTIONS, test_answers)
print(results)
```

## FAQ

**Q: Can I change the number of questions?**
A: Yes, add or remove questions in `exam_data.py`. The grading logic automatically adapts to the question count.

**Q: Are scores saved?**
A: No, the MVP does not persist scores. This feature is planned for v2.0 with user authentication.

**Q: Can I randomize question order?**
A: Not in the current version. Question randomization is a planned enhancement for v2.0.

**Q: Is there a time limit?**
A: No, users can take as long as needed. Timed mode is a future enhancement.

**Q: Can I use this for other trivia topics?**
A: Yes! Modify `exam_data.py` to replace NFL questions with any topic. The architecture is topic-agnostic.

**Q: How do I update question content?**
A: Edit `exam_data.py` directly. No database or migration required for the MVP.

**Q: Does this work offline?**
A: No, it requires a running Flask server. Future versions could implement offline capability with service workers.

## Future Enhancements (v2.0+)

Planned features for future releases:

### Authentication & Persistence
- User account creation and login
- Score history tracking with database storage
- Progress analytics and performance trends
- User profiles with customization

### Content Expansion
- Question bank expansion (50+ questions)
- Question randomization per attempt
- Difficulty level selection (Easy, Medium, Hard)
- Multiple exam categories (History, Current Season, Rules, Records)
- Question tagging and filtering

### Advanced Features
- Timed exam mode with countdown timer
- Leaderboard with rankings and badges
- Social sharing of scores
- Email notifications for score reports
- Admin dashboard for content management
- Question statistics and analytics
- Mobile app (iOS/Android)

### SaaS Enhancements
- Multi-tenancy support
- Subscription tiers (Free, Pro, Enterprise)
- Custom branding and white-labeling
- API for third-party integrations
- Advanced analytics and reporting dashboard
- A/B testing for questions
- Gamification elements (achievements, streaks)

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Contribution Guidelines:**
- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Test your changes thoroughly
- Update documentation as needed
- Keep commits focused and descriptive

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact & Support

**Project Maintainer**: Product Team

**Issues**: Please report bugs and feature requests via the project issue tracker

**Documentation**: Additional documentation available in PRD.md

**Community**: Join discussions and share feedback

## Acknowledgments

- NFL trivia content sourced from official NFL records
- Built with Flask web framework
- Inspired by modern educational assessment tools
- Designed for accessibility and user experience

---

**Version**: 1.0 (MVP)
**Last Updated**: November 5, 2025
**Status**: Production Ready

Made with dedication to NFL fans and trivia enthusiasts everywhere.
