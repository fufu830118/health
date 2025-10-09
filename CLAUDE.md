# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Application Overview

This is a modern Chinese health education quiz application built with Flask and advanced HTML/CSS/JavaScript. The application features a futuristic UI design with glassmorphism effects, Web Audio API sound system, comprehensive question management through Excel integration, and an exercise punishment video gallery system.

## Architecture

### Backend Structure
- **Flask Application** (`app.py`): Main server with REST API endpoints and console startup mode
- **Excel-based Question Management**:
  - Loads from `問答題庫範本.xlsx` with columns: 題號, 類別, 題目內容, 選項A/B/C, 正確答案, 出現過
  - 50 questions total, evenly distributed across 5 categories (10 questions each)
  - Tracks question usage with `出現過` column to prevent repetition
  - Real-time Excel updates marking questions as used
  - Smart category reset when all questions exhausted
- **Static File Serving**: Video and image files served from `影片/` directory via `/videos/<filename>` route

### Question Categories (5 Total)
The application supports exactly 5 question categories, each with 10 questions:
1. **環保題** (Environmental) - `fas fa-recycle` icon
2. **安全題** (Safety) - `fas fa-shield-alt` icon
3. **衛生題** (Hygiene) - `fas fa-hands-wash` icon
4. **健康題** (Health) - `fas fa-heartbeat` icon
5. **防災題** (Disaster Prevention) - `fas fa-exclamation-triangle` icon

### Frontend Structure
- **Futuristic Main Menu** (`index.html`):
  - Glassmorphism design with animated particle backgrounds
  - Dynamic category loading from API with custom FontAwesome icons
  - "運動懲罰示範" (Exercise Punishment Demo) button linking to video gallery
  - CSS Grid responsive layout with hover animations
  - Modern gradient text effects and glow animations

- **Exercise Punishment Gallery** (`punishment_videos.html`):
  - **FULLY COMMENTED CODE**: Every line has detailed Chinese comments explaining functionality
  - Grid layout displaying 8 exercise videos/images from `影片/` folder
  - Modal window for full-screen video playback
  - Supports both MP4 videos and JPG images
  - Automatic thumbnail generation with play/image icons
  - Click to play, ESC or background click to close

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

- `GET /` - Main menu page
- `GET /question_display` - Question display page
- `GET /punishment_videos` - Exercise punishment video gallery page
- `GET /videos/<filename>` - Serves video/image files from `影片/` directory
- `GET /api/categories` - Returns array of 5 question categories from Excel
- `GET /api/questions?category={category}` - Returns random unused question from specified category
- `POST /api/check_answer` - Validates answer and returns feedback with redirect URL
- `POST /api/clear_session` - Clears session data (legacy support)

## Common Development Commands

### Running the Application
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows

# Install dependencies (first time only)
pip install -r requirements.txt

# Run Flask application (console mode - recommended)
python app.py

# Access at http://127.0.0.1:5000
# Server runs on port 5000 in debug mode
```

### Windows Quick Start
```bash
# Use batch file for one-click startup
start_health_quiz.bat
```

### Restarting After Changes
When you modify Excel data or Python code:
1. Stop server (Ctrl+C in terminal)
2. Run `python app.py` again
3. Refresh browser to see changes

**Note**: Excel changes require server restart because data is loaded at startup in `app.py` line 72.

## File Organization

### Core Application Files
- `app.py` - Flask application with video serving routes
- `requirements.txt` - Python dependencies (Flask 2.3.2, pandas, openpyxl)
- `問答題庫範本.xlsx` - Excel question database (50 questions, 5 categories)
- `影片/` - Exercise videos and images directory (8 files)

### HTML Templates
All HTML files use:
- **Tailwind CSS** via CDN for utility-first styling
- **FontAwesome 6** for modern icons
- **Microsoft JhengHei** font for Chinese text rendering
- **Dark Theme**: Futuristic color scheme with cyan/purple/pink/red accents
- **Glassmorphism Effects**: Backdrop filters and transparent designs
- **CSS Custom Properties**: Centralized theming in `:root`

### Styling Architecture
- **CSS Variables**: Centralized in `:root` selector
  - `--primary-bg`, `--secondary-bg`, `--accent-cyan`, `--accent-purple`, `--accent-pink`, `--accent-red`
  - `--text-primary`, `--text-secondary`, `--glass-bg`
- **Responsive Breakpoints**: 768px (tablet), 480px (mobile)
- **Animation System**: Keyframe-based hover effects and transitions
- **Component-based Styling**: Reusable `.category-button`, `.glass-container`, `.video-card` classes

## Application Flow

1. **Startup**: Console mode with Flask development server on port 5000
2. **Main Menu**: 5 category buttons + 1 exercise video gallery button
3. **Category Selection**: Click category to start quiz OR click exercise button to view videos
4. **Question Display**: Random unused question with 30-second animated countdown
5. **Audio Feedback**: Web Audio API provides contextual sound effects
6. **Answer Submission**: Immediate feedback with animated transitions
7. **Progress Tracking**: Excel-based usage tracking prevents repetition
8. **Category Completion**: Auto-redirect when all 10 questions in category answered

## Technical Implementation Details

### Sound System Architecture
- **Web Audio API**: Pure JavaScript tone generation
- **Sound Types**: click, hover, tick, warning, critical, timeout, success, error
- **Context Management**: User-initiated audio context for browser compatibility
- **Progressive Enhancement**: Graceful degradation when audio unavailable

### Excel Integration
- **openpyxl Library**: Direct Excel file manipulation
- **Real-time Updates**: Marks questions as used via `mark_question_as_used()` function
- **Category-based Loading**: `load_questions_fresh_from_excel()` reads latest state
- **Error Handling**: Graceful fallback for missing columns or data

### Video Gallery System
- **Static File Serving**: Flask `send_from_directory()` serves files from `影片/` folder
- **Modal System**: Full-screen overlay for video playback
- **Responsive Grid**: CSS Grid with `repeat(auto-fill, minmax(320px, 1fr))`
- **Media Detection**: Automatically handles both video and image file types
- **Event Handling**: Click, ESC key, and background click to close modal

### Responsive Design Strategy
- **Mobile-First**: Base styles optimized for mobile devices
- **Progressive Enhancement**: Desktop features added via media queries
- **Touch-Friendly**: Large buttons and touch targets on mobile
- **Performance**: Optimized animations and transitions

## Development Notes

### Adding New Question Categories
**IMPORTANT**: This app is designed for exactly 5 categories. To change categories:

1. **Update Excel file** (`問答題庫範本.xlsx`):
   - Modify `類別` column with new category name
   - Maintain 10 questions per category for balance

2. **Update icon mapping** in `index.html`:
   ```javascript
   const categoryIcons = {
       '新類別名稱': 'fas fa-icon-name',  // Add new category
       // ... other categories
   };
   ```

3. **Restart Flask server** to reload Excel data

4. API will automatically detect and serve new categories (no code change needed)

### Modifying Exercise Video Gallery
**Location**: `punishment_videos.html` (fully commented)

To add/remove videos:
1. Update `mediaFiles` array in JavaScript section (line ~368)
2. Add video/image files to `影片/` directory
3. No server restart needed (static files)

### Customizing UI Theme
- **Colors**: Modify CSS `:root` variables in any HTML file
- **Glassmorphism**: Adjust `backdrop-filter: blur()` values
- **Animations**: Edit `@keyframes` definitions
- **Icons**: Change FontAwesome classes in `categoryIcons` object

### Audio System Modifications
- **Location**: `question_display.html` > `SoundManager` class
- **Add sounds**: Extend `sounds` object with new {frequency, duration, type}
- **Adjust tones**: Modify frequency values (in Hz)
- **Timing**: Change duration values (in milliseconds)

### Code Documentation Standards
- `punishment_videos.html` serves as the **documentation example** - every line has detailed Chinese comments
- When creating new HTML pages, follow the same commenting style
- Use section dividers like `/* =========== Section Name =========== */`
- Explain WHY not just WHAT (e.g., "絕對定位在右上角" instead of just "position: absolute")

## Deployment Considerations
- **PyInstaller Ready**: Supports packaging as standalone executable
- **Path Resolution**: Handles both development and packaged environments via `getattr(sys, 'frozen', False)`
- **Asset Management**: Tailwind CSS and FontAwesome loaded via CDN
- **Cross-Platform**: Windows batch file + Python cross-platform core
- **Video Files**: Ensure `影片/` directory is included in deployment package
