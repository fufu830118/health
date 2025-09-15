# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Application Overview

This is a Chinese health education quiz application built with Flask and HTML/CSS/JavaScript. The application presents categorized health questions with multiple-choice answers and provides immediate feedback. It features a desktop-style interface with a Tkinter launcher and can be packaged as a standalone executable.

## Architecture

### Backend Structure
- **Flask Application** (`app.py`): Main server with REST API endpoints and Tkinter GUI launcher
- **Question Data**: Loaded from Excel file (`問答題庫範本.xlsx`) with structure:
  - 類別 (Category)
  - 題目內容 (Question Content)
  - 選項A/B/C (Options A/B/C)
  - 正確答案 (Correct Answer: A/B/C)
- **Session Management**: Tracks asked questions per category to avoid repetition

### Frontend Structure
- **Main Menu** (`index.html`): Category selection interface
- **Question Display** (`question_display.html`): Question presentation with 30-second countdown timer
- **Feedback Pages**: 
  - `feedback_correct.html` - Correct answer feedback
  - `feedback_incorrect.html` - Incorrect answer feedback
  - `timeout_feedback.html` - Time-out feedback

### Key Features
- **Question Randomization**: Questions are randomly selected from categories, avoiding repetition until all questions in a category are exhausted
- **Countdown Timer**: 30-second timer with visual warning at 10 seconds remaining
- **Session Persistence**: Flask sessions track which questions have been asked per category
- **Responsive Design**: Optimized for different screen sizes with Tailwind CSS
- **Desktop Launcher**: Tkinter interface for starting the web server

## API Endpoints

- `GET /api/categories` - Returns list of available question categories
- `GET /api/questions?category={category}` - Returns random question from specified category
- `POST /api/check_answer` - Validates answer and returns feedback

## Common Development Commands

### Running the Application
```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask application with GUI launcher
python app.py

# Run Flask server directly (development mode)
python -c "from app import app; app.run(debug=True)"
```

### Using the Batch File
```bash
# Windows batch file for backend startup (expects virtual environment)
start_backend.bat
```

## File Organization

### Core Application Files
- `app.py` - Main Flask application with Tkinter launcher
- `requirements.txt` - Python dependencies (Flask 2.3.2, openpyxl 3.1.2)

### Templates (HTML Files)
All HTML files are located in the root directory and use:
- Tailwind CSS via CDN
- Font Awesome icons
- Microsoft JhengHei font family
- Dark theme (#1a202c background)
- Responsive design with mobile breakpoints

### Question Database
- `問答題庫範本.xlsx` - Excel file containing categorized questions
- Expected columns: 類別, 題目內容, 選項A, 選項B, 選項C, 正確答案

## Application Flow

1. **Launch**: Tkinter GUI starts Flask server on port 5000
2. **Category Selection**: User selects question category from dynamically loaded buttons
3. **Question Display**: Random question shown with 30-second countdown
4. **Answer Submission**: User selects answer and submits before timeout
5. **Feedback**: Appropriate feedback page shown based on correctness
6. **Return to Menu**: User can return to category selection

## Styling Consistency

The application maintains consistent styling across all pages:
- **Button Sizes**: 2.5rem font, 1.5rem×2.5rem padding
- **Large Text**: 4-4.5rem for main titles and messages
- **Colors**: Green (#4CAF50) for correct/primary, Red (#DC3545) for incorrect, Blue (#4299e1) for neutral
- **Responsive Breakpoints**: 768px (medium), 480px (small)

## Development Notes

### Session Management
Questions are tracked in Flask sessions to prevent immediate repetition. When all questions in a category are exhausted, the session resets for that category.

### Executable Packaging
The application is designed to be packaged with PyInstaller:
- Uses `sys.frozen` detection for executable vs development paths
- Template directory path resolution for both modes
- Question file path resolution for both modes

### Template Directory Configuration
The Flask app expects templates in a specific structure when packaged:
- Development: `../design/prototypes/` relative to `app.py`
- Packaged: `design/prototypes/` within the executable bundle