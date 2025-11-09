#!/usr/bin/env python3
"""
Hindi Typing Master - Offline Application
A complete typing tutor for Hindi (Devanagari) with support for multiple keyboard layouts
"""

from flask import Flask, render_template, jsonify, request, session
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)

# Database setup
DB_PATH = 'typing_master.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with schema"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            layout_pref TEXT DEFAULT 'inscript',
            font_pref TEXT DEFAULT 'unicode',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Lessons table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content_unicode TEXT NOT NULL,
            content_kruti TEXT,
            difficulty TEXT DEFAULT 'beginner',
            category TEXT,
            tags TEXT,
            order_num INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            lesson_id INTEGER,
            layout_used TEXT,
            raw_input TEXT,
            expected_text TEXT,
            wpm REAL,
            accuracy REAL,
            errors_json TEXT,
            time_taken INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (lesson_id) REFERENCES lessons (id)
        )
    ''')
    
    # Stats aggregates table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats_aggregates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            metric TEXT,
            value REAL,
            date DATE,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Leaderboard/high scores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            lesson_id INTEGER,
            wpm REAL,
            accuracy REAL,
            achieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (lesson_id) REFERENCES lessons (id)
        )
    ''')
    
    conn.commit()
    
    # Add sample lessons if empty
    cursor.execute('SELECT COUNT(*) as count FROM lessons')
    if cursor.fetchone()['count'] == 0:
        insert_sample_lessons(conn)
    
    conn.close()

def insert_sample_lessons(conn):
    """Insert sample lessons for practice"""
    lessons = [
        {
            'title': 'स्वर परिचय (Vowels Introduction)',
            'content': 'अ आ इ ई उ ऊ ए ऐ ओ औ अं अः',
            'difficulty': 'beginner',
            'category': 'basics',
            'order': 1
        },
        {
            'title': 'व्यंजन परिचय (Consonants - Part 1)',
            'content': 'क ख ग घ ङ च छ ज झ ञ ट ठ ड ढ ण त थ द ध न',
            'difficulty': 'beginner',
            'category': 'basics',
            'order': 2
        },
        {
            'title': 'व्यंजन परिचय (Consonants - Part 2)',
            'content': 'प फ ब भ म य र ल व श ष स ह क्ष त्र ज्ञ',
            'difficulty': 'beginner',
            'category': 'basics',
            'order': 3
        },
        {
            'title': 'मात्राएं (Matras - Vowel Signs)',
            'content': 'का की कु कू के कै को कौ कं कः',
            'difficulty': 'beginner',
            'category': 'matras',
            'order': 4
        },
        {
            'title': 'सरल शब्द (Simple Words)',
            'content': 'मन धन जन तन वन सब कब जब तब रथ पथ नल बल फल हल',
            'difficulty': 'beginner',
            'category': 'words',
            'order': 5
        },
        {
            'title': 'दो अक्षर के शब्द (Two Letter Words)',
            'content': 'घर कर नर दर पर बस रस कस बन मन धन जन वन सन रन कन',
            'difficulty': 'beginner',
            'category': 'words',
            'order': 6
        },
        {
            'title': 'तीन अक्षर के शब्द (Three Letter Words)',
            'content': 'गरम नरम करम परम धरम शरम बरस तरस परस फसल हसन गमन नमन समय',
            'difficulty': 'intermediate',
            'category': 'words',
            'order': 7
        },
        {
            'title': 'संयुक्त अक्षर (Conjunct Characters)',
            'content': 'क्ष त्र ज्ञ श्र स्त्र क्त व्य स्व प्र द्ध त्त द्य द्व द्ध न्न म्म',
            'difficulty': 'intermediate',
            'category': 'conjuncts',
            'order': 8
        },
        {
            'title': 'छोटे वाक्य (Short Sentences)',
            'content': 'राम घर गया। वह खाना खाता है। मैं स्कूल जाता हूं। यह बहुत अच्छा है।',
            'difficulty': 'intermediate',
            'category': 'sentences',
            'order': 9
        },
        {
            'title': 'दिन और समय (Days and Time)',
            'content': 'सोमवार मंगलवार बुधवार गुरुवार शुक्रवार शनिवार रविवार सुबह दोपहर शाम रात',
            'difficulty': 'intermediate',
            'category': 'vocabulary',
            'order': 10
        },
        {
            'title': 'रंग और संख्याएं (Colors and Numbers)',
            'content': 'लाल नीला हरा पीला काला सफेद एक दो तीन चार पांच छह सात आठ नौ दस',
            'difficulty': 'intermediate',
            'category': 'vocabulary',
            'order': 11
        },
        {
            'title': 'परिवार (Family)',
            'content': 'माता पिता भाई बहन दादा दादी नाना नानी चाचा चाची मामा मामी बेटा बेटी',
            'difficulty': 'intermediate',
            'category': 'vocabulary',
            'order': 12
        },
        {
            'title': 'लंबे वाक्य (Long Sentences)',
            'content': 'भारत एक विशाल देश है। यहां विभिन्न भाषाएं बोली जाती हैं। हमें अपनी संस्कृति पर गर्व होना चाहिए।',
            'difficulty': 'advanced',
            'category': 'sentences',
            'order': 13
        },
        {
            'title': 'कहानी अभ्यास (Story Practice)',
            'content': 'एक बार की बात है। एक गांव में एक किसान रहता था। वह बहुत मेहनती था। उसके पास एक छोटा सा खेत था। वह प्रतिदिन मेहनत करता था।',
            'difficulty': 'advanced',
            'category': 'paragraph',
            'order': 14
        },
        {
            'title': 'समाचार पत्र शैली (Newspaper Style)',
            'content': 'आज के युग में प्रौद्योगिकी का महत्व बढ़ता जा रहा है। शिक्षा के क्षेत्र में भी डिजिटल माध्यम का उपयोग तेजी से बढ़ रहा है।',
            'difficulty': 'advanced',
            'category': 'paragraph',
            'order': 15
        }
    ]
    
    cursor = conn.cursor()
    for lesson in lessons:
        cursor.execute('''
            INSERT INTO lessons (title, content_unicode, difficulty, category, order_num)
            VALUES (?, ?, ?, ?, ?)
        ''', (lesson['title'], lesson['content'], lesson['difficulty'], lesson['category'], lesson['order']))
    
    conn.commit()

# Routes
@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/test')
def test_page():
    """Keyboard test page"""
    return render_template('test.html')

@app.route('/api/register', methods=['POST'])
def register():
    """Register new user"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email', '')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        password_hash = generate_password_hash(password)
        cursor.execute('''
            INSERT INTO users (username, password_hash, email)
            VALUES (?, ?, ?)
        ''', (username, password_hash, email))
        conn.commit()
        user_id = cursor.lastrowid
        
        session['user_id'] = user_id
        session['username'] = username
        
        conn.close()
        return jsonify({'success': True, 'user_id': user_id, 'username': username})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Username already exists'}), 400

@app.route('/api/login', methods=['POST'])
def login():
    """Login user"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user['password_hash'], password):
        session['user_id'] = user['id']
        session['username'] = user['username']
        return jsonify({
            'success': True,
            'user_id': user['id'],
            'username': user['username'],
            'layout_pref': user['layout_pref'],
            'font_pref': user['font_pref']
        })
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({'success': True})

@app.route('/api/user/profile', methods=['GET'])
def get_profile():
    """Get user profile"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email, layout_pref, font_pref, created_at FROM users WHERE id = ?', 
                   (session['user_id'],))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify(dict(user))
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/user/preferences', methods=['PUT'])
def update_preferences():
    """Update user preferences"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.json
    layout_pref = data.get('layout_pref')
    font_pref = data.get('font_pref')
    
    conn = get_db()
    cursor = conn.cursor()
    
    if layout_pref:
        cursor.execute('UPDATE users SET layout_pref = ? WHERE id = ?', 
                      (layout_pref, session['user_id']))
    if font_pref:
        cursor.execute('UPDATE users SET font_pref = ? WHERE id = ?', 
                      (font_pref, session['user_id']))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/lessons', methods=['GET'])
def get_lessons():
    """Get all lessons"""
    difficulty = request.args.get('difficulty')
    category = request.args.get('category')
    
    conn = get_db()
    cursor = conn.cursor()
    
    query = 'SELECT * FROM lessons WHERE 1=1'
    params = []
    
    if difficulty:
        query += ' AND difficulty = ?'
        params.append(difficulty)
    if category:
        query += ' AND category = ?'
        params.append(category)
    
    query += ' ORDER BY order_num, id'
    
    cursor.execute(query, params)
    lessons = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(lessons)

@app.route('/api/lessons/<int:lesson_id>', methods=['GET'])
def get_lesson(lesson_id):
    """Get specific lesson"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM lessons WHERE id = ?', (lesson_id,))
    lesson = cursor.fetchone()
    conn.close()
    
    if lesson:
        return jsonify(dict(lesson))
    return jsonify({'error': 'Lesson not found'}), 404

@app.route('/api/sessions', methods=['POST'])
def save_session():
    """Save typing session"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.json
    lesson_id = data.get('lesson_id')
    layout_used = data.get('layout_used')
    raw_input = data.get('raw_input')
    expected_text = data.get('expected_text')
    wpm = data.get('wpm')
    accuracy = data.get('accuracy')
    errors = data.get('errors', [])
    time_taken = data.get('time_taken')
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO sessions (user_id, lesson_id, layout_used, raw_input, expected_text, 
                             wpm, accuracy, errors_json, time_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (session['user_id'], lesson_id, layout_used, raw_input, expected_text, 
          wpm, accuracy, json.dumps(errors), time_taken))
    
    session_id = cursor.lastrowid
    
    # Update aggregated stats
    today = datetime.now().date()
    cursor.execute('''
        INSERT OR REPLACE INTO stats_aggregates (user_id, metric, value, date)
        VALUES (?, 'avg_wpm', ?, ?)
    ''', (session['user_id'], wpm, today))
    
    cursor.execute('''
        INSERT OR REPLACE INTO stats_aggregates (user_id, metric, value, date)
        VALUES (?, 'avg_accuracy', ?, ?)
    ''', (session['user_id'], accuracy, today))
    
    # Update leaderboard if this is a high score
    cursor.execute('''
        SELECT MAX(wpm) as max_wpm FROM leaderboard 
        WHERE user_id = ? AND lesson_id = ?
    ''', (session['user_id'], lesson_id))
    result = cursor.fetchone()
    
    if not result['max_wpm'] or wpm > result['max_wpm']:
        cursor.execute('''
            INSERT INTO leaderboard (user_id, lesson_id, wpm, accuracy)
            VALUES (?, ?, ?, ?)
        ''', (session['user_id'], lesson_id, wpm, accuracy))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'session_id': session_id})

@app.route('/api/stats/user', methods=['GET'])
def get_user_stats():
    """Get user statistics"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Overall stats
    cursor.execute('''
        SELECT 
            COUNT(*) as total_sessions,
            AVG(wpm) as avg_wpm,
            MAX(wpm) as max_wpm,
            AVG(accuracy) as avg_accuracy,
            MAX(accuracy) as max_accuracy,
            SUM(time_taken) as total_time
        FROM sessions WHERE user_id = ?
    ''', (session['user_id'],))
    overall = dict(cursor.fetchone())
    
    # Recent sessions
    cursor.execute('''
        SELECT s.*, l.title as lesson_title
        FROM sessions s
        LEFT JOIN lessons l ON s.lesson_id = l.id
        WHERE s.user_id = ?
        ORDER BY s.created_at DESC
        LIMIT 10
    ''', (session['user_id'],))
    recent = [dict(row) for row in cursor.fetchall()]
    
    # Progress over time
    cursor.execute('''
        SELECT date, metric, value
        FROM stats_aggregates
        WHERE user_id = ?
        ORDER BY date DESC
        LIMIT 30
    ''', (session['user_id'],))
    progress = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({
        'overall': overall,
        'recent': recent,
        'progress': progress
    })

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get leaderboard"""
    lesson_id = request.args.get('lesson_id', type=int)
    limit = request.args.get('limit', 10, type=int)
    
    conn = get_db()
    cursor = conn.cursor()
    
    query = '''
        SELECT l.*, u.username, les.title as lesson_title
        FROM leaderboard l
        JOIN users u ON l.user_id = u.id
        LEFT JOIN lessons les ON l.lesson_id = les.id
        WHERE 1=1
    '''
    params = []
    
    if lesson_id:
        query += ' AND l.lesson_id = ?'
        params.append(lesson_id)
    
    query += ' ORDER BY l.wpm DESC, l.accuracy DESC LIMIT ?'
    params.append(limit)
    
    cursor.execute(query, params)
    leaderboard = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(leaderboard)

@app.route('/api/analytics/errors', methods=['GET'])
def get_error_analytics():
    """Get error analytics for user"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT errors_json, created_at
        FROM sessions
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT 50
    ''', (session['user_id'],))
    
    sessions = cursor.fetchall()
    conn.close()
    
    # Aggregate errors
    error_counts = {}
    for row in sessions:
        if row['errors_json']:
            errors = json.loads(row['errors_json'])
            for error in errors:
                char = error.get('expected', '')
                if char:
                    error_counts[char] = error_counts.get(char, 0) + 1
    
    # Sort by frequency
    sorted_errors = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)
    
    return jsonify({
        'error_heatmap': sorted_errors[:20],  # Top 20 most problematic characters
        'total_errors': sum(error_counts.values())
    })

if __name__ == '__main__':
    # Initialize database
    if not os.path.exists(DB_PATH):
        init_db()
        print("Database initialized successfully!")
    
    print("\n" + "="*60)
    print("Hindi Typing Master - Starting Application")
    print("="*60)
    print("\nAccess the application at: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
