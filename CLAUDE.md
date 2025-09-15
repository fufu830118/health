# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Application Overview

This is a modern Chinese health education quiz application built with Flask and advanced HTML/CSS/JavaScript. The application features a futuristic UI design with glassmorphism effects, Web Audio API sound system, and comprehensive question management through Excel integration.

## Architecture

### Backend Structure
- **Flask Application** (`app.py`): Main server with REST API endpoints and console startup mode
- **Excel-based Question Management**: 
  - Loads from `問答題庫範本.xlsx` with columns: 類別, 題目內容, 選項A/B/C, 正確答案
  - Tracks question usage with `出現過` column to prevent repetition
  - Real-time Excel updates marking questions as used
  - Smart category reset when all questions exhausted
- **Advanced Session Management**: Direct Excel tracking instead of Flask sessions for persistence

### Frontend Structure
- **Futuristic Main Menu** (`index.html`): 
  - Glassmorphism design with animated particle backgrounds
  - Dynamic category loading with custom icons (FontAwesome integration)
  - CSS Grid responsive layout with hover animations
  - Modern gradient text effects and glow animations
- **Advanced Question Display** (`question_display.html`):
  - 30-second countdown timer with visual warnings (10s yellow, 5s red)
  - Web Audio API sound system generating tones without external files
  - Interactive option selection with glassmorphism buttons
  - Real-time visual feedback and animations
- **Enhanced Feedback System**: 
  - `feedback_correct.html` - Success feedback with animations
  - `feedback_incorrect.html` - Incorrect answer feedback  
  - `timeout_feedback.html` - Time-out handling
  - `no_more_questions.html` - Category completion notification

### Modern UI Features
- **Glassmorphism Design**: Backdrop blur effects with semi-transparent containers
- **Dynamic Particle Background**: Pure CSS animated floating particles
- **Web Audio API Sound System**: 
  - Real-time tone generation (no external audio files)
  - Context-aware sound effects (tick, warning, success, error)
  - User interaction-triggered audio context initialization
- **Advanced Responsive Design**: Mobile-first approach with Tailwind CSS
- **Smooth Animations**: CSS transitions, transforms, and keyframe animations

## API Endpoints

- `GET /api/categories` - Returns available question categories
- `GET /api/questions?category={category}` - Returns random unused question from category
- `POST /api/check_answer` - Validates answer and returns feedback with redirect
- `POST /api/clear_session` - Clears session data (legacy support)

## Common Development Commands

### Running the Application
```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask application (console mode - recommended)
python app.py

# Alternative: Run with GUI launcher (if Tkinter available)
# The app detects environment and runs console mode by default
```

### Using Batch Files
```bash
# Windows batch file for easy startup
start_health_quiz.bat
```

## File Organization

### Core Application Files
- `app.py` - Flask application with console startup and Tkinter GUI fallback
- `requirements.txt` - Python dependencies (Flask 2.3.2, pandas, openpyxl)
- `問答題庫範本.xlsx` - Excel question database with usage tracking

### Modern HTML Templates
All HTML files use:
- **Tailwind CSS** via CDN for utility-first styling
- **FontAwesome 6** for modern icons
- **Microsoft JhengHei** font for Chinese text rendering
- **Dark Theme**: Futuristic color scheme with cyan/purple/pink accents
- **Glassmorphism Effects**: Backdrop filters and transparent designs
- **CSS Custom Properties**: Centralized theming variables

### Styling Architecture
- **CSS Variables**: Centralized color and sizing systems
- **Responsive Breakpoints**: 768px (tablet), 480px (mobile)
- **Animation System**: Keyframe-based hover effects and transitions
- **Component-based Styling**: Reusable button and container classes

## Application Flow

1. **Startup**: Console mode with Flask development server on port 5000
2. **Category Selection**: Dynamic category buttons with icons and animations
3. **Question Display**: Random question with 30-second animated countdown
4. **Audio Feedback**: Web Audio API provides contextual sound effects
5. **Answer Submission**: Immediate feedback with animated transitions
6. **Progress Tracking**: Excel-based usage tracking prevents repetition
7. **Category Completion**: Auto-redirect when all questions answered

## Technical Implementation Details

### Sound System Architecture
- **Web Audio API**: Pure JavaScript tone generation
- **Sound Types**: click, hover, tick, warning, critical, timeout, success, error
- **Context Management**: User-initiated audio context for browser compatibility
- **Progressive Enhancement**: Graceful degradation when audio unavailable

### Excel Integration
- **openpyxl Library**: Direct Excel file manipulation
- **Real-time Updates**: Marks questions as used immediately
- **Error Handling**: Graceful fallback for missing columns or data
- **Category Management**: Automatic reset when all questions exhausted

### Responsive Design Strategy
- **Mobile-First**: Base styles optimized for mobile devices
- **Progressive Enhancement**: Desktop features added via media queries
- **Touch-Friendly**: Large buttons and touch targets on mobile
- **Performance**: Optimized animations and transitions

### Deployment Considerations
- **PyInstaller Ready**: Supports packaging as standalone executable
- **Path Resolution**: Handles both development and packaged environments
- **Asset Management**: All assets via CDN for simplified deployment
- **Cross-Platform**: Windows batch file + Python cross-platform core

## Development Notes

### Adding New Question Categories
1. Add new category to Excel file `類別` column
2. Ensure FontAwesome icon mapping in `index.html` (optional)
3. Questions automatically available without code changes

### Customizing UI Theme
- Modify CSS custom properties in `:root` selectors
- Update Tailwind classes for consistent theming
- Adjust glassmorphism backdrop-filter values

### Audio System Modifications
- Edit `SoundManager` class in `question_display.html`
- Adjust frequency/duration values for different sound effects
- Add new sound types by extending the `sounds` object