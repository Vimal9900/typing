# Hindi Typing Master - हिंदी टाइपिंग मास्टर

A complete, offline Hindi typing tutor application with support for multiple keyboard layouts and fonts.

## Features

✨ **Complete Typing Tutor**
- 15+ structured lessons from beginner to advanced
- Real-time WPM (Words Per Minute) tracking
- Accuracy measurement and error tracking
- Timed tests (1, 2, and 5 minutes)

⌨️ **Multiple Keyboard Layouts**
- **InScript** - Standard Indian keyboard layout
- **Remington** - Traditional layout for Kruti Dev
- **Transliteration** - Type in Roman letters, get Hindi output

🔤 **Font Support**
- **Unicode Devanagari** (Mangal) - Modern standard
- **Kruti Dev** - Legacy font support with bidirectional converter

📊 **Analytics & Progress Tracking**
- Session history with detailed statistics
- Error heatmap showing problematic characters
- Progress charts over time
- Personal best records

🏆 **Gamification**
- Leaderboard system
- Personal high scores
- Multiple difficulty levels

🔒 **Offline First**
- No internet required after setup
- SQLite database - no external database needed
- All data stored locally
- Complete privacy

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Steps

1. **Navigate to the project directory:**
   ```bash
   cd /home/mandar/data-storage/Vimal/Hinditypemaster/codebase
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open your browser:**
   Navigate to `http://localhost:5000`

That's it! The application will automatically create the database and populate it with sample lessons on first run.

## Usage

### First Time Setup

1. **Register an Account**
   - Click "Register" on the home page
   - Create a username and password
   - Your data is stored locally and privately

2. **Choose Your Preferences**
   - Select keyboard layout (InScript/Remington/Transliteration)
   - Choose font preference (Unicode/Kruti Dev)
   - These can be changed anytime from the dashboard

3. **Start Learning**
   - Begin with beginner lessons to learn character placement
   - Progress through intermediate lessons for words and phrases
   - Challenge yourself with advanced lessons and timed tests

### Keyboard Layouts

#### InScript
The standard Indian keyboard layout, logical and efficient for Hindi typing.
- Vowels on the left (QWERT keys)
- Consonants on the right and home row
- Use Shift for aspirated consonants

#### Remington
Traditional layout commonly used with Kruti Dev font.
- Popular in government offices
- Different arrangement from InScript
- Requires practice but efficient for experienced users

#### Transliteration
Type in Roman letters and get Hindi automatically.
- Most intuitive for beginners
- Examples:
  - "namaste" → "नमस्ते"
  - "bharat" → "भारत"
  - "hindi" → "हिंदी"

### Practice Modes

1. **Lessons** - Structured learning path with 15+ lessons
2. **Practice** - Free practice mode with any lesson
3. **Test** - Timed tests to measure your speed and accuracy

## Features in Detail

### Real-time Feedback
- Characters highlighted as you type (green = correct, red = incorrect)
- Live WPM and accuracy calculations
- Virtual keyboard shows which keys to press

### Analytics Dashboard
- View all your practice sessions
- See your most problematic characters
- Track improvement over time
- Compare with other users on the leaderboard

### Error Analysis
- Detailed tracking of typing errors
- Heatmap of characters you struggle with
- Personalized recommendations for practice

## Technical Details

### Technology Stack
- **Backend**: Python + Flask
- **Database**: SQLite (embedded, no setup needed)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla JS)
- **No external services**: Everything runs locally

### Database Schema
- **users** - User accounts and preferences
- **lessons** - Lesson content (pre-populated)
- **sessions** - Practice session records
- **stats_aggregates** - Daily statistics
- **leaderboard** - High scores

### File Structure
```
codebase/
├── app.py                    # Main Flask application
├── kruti_converter.py        # Kruti Dev ↔ Unicode converter
├── requirements.txt          # Python dependencies
├── typing_master.db          # SQLite database (created on first run)
├── templates/
│   └── index.html           # Main HTML template
└── static/
    ├── style.css            # Styles
    ├── app.js              # Main JavaScript logic
    └── keyboards.js        # Keyboard layouts and mappings
```

## Kruti Dev Support

The application includes a bidirectional converter between Kruti Dev (legacy font) and Unicode Devanagari.

### Using Kruti Dev
1. Select "Kruti Dev" from the font selector
2. Content will be displayed in Kruti Dev format
3. The converter automatically handles the conversion

### Converter Features
- Bidirectional conversion (Kruti ↔ Unicode)
- Handles complex characters and conjuncts
- Automatic encoding detection
- Preserves formatting

## Tips for Learning

1. **Start Slow**: Focus on accuracy first, speed will come naturally
2. **Proper Posture**: Sit up straight, feet flat on the floor
3. **Home Row**: Keep fingers on home row (ASDF for left, JKL; for right)
4. **Don't Look**: Try to type without looking at the keyboard
5. **Practice Daily**: 15-30 minutes daily is better than occasional long sessions
6. **Use All Fingers**: Learn proper finger placement for each key
7. **Error Analysis**: Review your error heatmap and practice problem characters

## Customization

### Adding Custom Lessons

You can add custom lessons by directly inserting into the database:

```python
import sqlite3
conn = sqlite3.connect('typing_master.db')
cursor = conn.cursor()

cursor.execute('''
    INSERT INTO lessons (title, content_unicode, difficulty, category, order_num)
    VALUES (?, ?, ?, ?, ?)
''', ('My Custom Lesson', 'Your Hindi text here', 'beginner', 'custom', 100))

conn.commit()
conn.close()
```

### Modifying Keyboard Layouts

Edit `static/keyboards.js` to customize or add keyboard layouts.

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

### Database Issues
Delete `typing_master.db` and restart the app. It will create a fresh database.

### Font Not Displaying
Make sure your system has Hindi fonts installed:
- **Windows**: Mangal (included by default)
- **Linux**: Install `fonts-indic` package
- **Mac**: Install Devanagari fonts from Font Book

### Browser Compatibility
Works best on modern browsers:
- Chrome 90+
- Firefox 88+
- Edge 90+
- Safari 14+

## Privacy & Security

- All data stored locally on your computer
- No external API calls or data transmission
- No analytics or tracking
- Your typing data never leaves your machine
- Open source - inspect the code yourself

## Performance

- Lightweight application (< 5MB total)
- Runs smoothly on low-end hardware
- Minimal system resources required
- Fast startup time
- No internet latency

## Future Enhancements (Optional)

Ideas you can implement:
- Export/import lessons
- Custom lesson creation through UI
- Sound effects and animations
- Certificate generation
- Multiplayer mode (local network)
- Mobile-responsive design improvements
- Dark mode theme
- More keyboard layouts
- Voice feedback

## License

This is a free, open-source educational tool. Use, modify, and distribute freely.

## Credits

Developed for Hindi learners who want a complete, offline, privacy-respecting typing tutor.

## Support

For issues or questions:
1. Check this README thoroughly
2. Review the code comments in `app.py`
3. Test with a fresh database
4. Check console logs in browser Developer Tools (F12)

---

**Happy Typing! शुभ टाइपिंग!** 🎉

Start your Hindi typing journey today and become a proficient typist!
