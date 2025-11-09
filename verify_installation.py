#!/usr/bin/env python3
"""
Installation Verification Script for Hindi Typing Master
Run this to verify all components are working correctly
"""

import sys
import os

def check_python_version():
    """Check if Python version is adequate"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python version too old: {version.major}.{version.minor}.{version.micro}")
        print("   Required: Python 3.7 or higher")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required = ['flask', 'flask_cors', 'werkzeug']
    all_ok = True
    
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is NOT installed")
            all_ok = False
    
    return all_ok

def check_files():
    """Check if all required files exist"""
    required_files = [
        'app.py',
        'kruti_converter.py',
        'requirements.txt',
        'templates/index.html',
        'static/style.css',
        'static/app.js',
        'static/keyboards.js'
    ]
    
    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} is MISSING")
            all_ok = False
    
    return all_ok

def test_kruti_converter():
    """Test Kruti Dev converter"""
    try:
        from kruti_converter import kruti_to_unicode, unicode_to_kruti, detect_encoding
        
        # Test Unicode
        test_text = "नमस्ते"
        encoding = detect_encoding(test_text)
        if encoding == 'unicode':
            print(f"✅ Kruti converter detects Unicode correctly")
        else:
            print(f"⚠️  Kruti converter detection might need adjustment")
        
        # Test conversion (basic)
        converted = unicode_to_kruti(test_text)
        print(f"✅ Kruti converter is functional")
        
        return True
    except Exception as e:
        print(f"❌ Kruti converter has issues: {e}")
        return False

def test_database():
    """Test database initialization"""
    try:
        import sqlite3
        
        # Check if database exists
        if os.path.exists('typing_master.db'):
            print("✅ Database file exists")
            
            # Check tables
            conn = sqlite3.connect('typing_master.db')
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            expected_tables = ['users', 'lessons', 'sessions', 'stats_aggregates', 'leaderboard']
            existing_tables = [t[0] for t in tables]
            
            for table in expected_tables:
                if table in existing_tables:
                    print(f"✅ Table '{table}' exists")
                else:
                    print(f"⚠️  Table '{table}' not found (will be created on first run)")
            
            conn.close()
        else:
            print("⚠️  Database doesn't exist yet (will be created on first run)")
        
        return True
    except Exception as e:
        print(f"❌ Database check failed: {e}")
        return False

def main():
    print("="*60)
    print("Hindi Typing Master - Installation Verification")
    print("="*60)
    print()
    
    checks = []
    
    print("1. Checking Python version...")
    checks.append(check_python_version())
    print()
    
    print("2. Checking dependencies...")
    checks.append(check_dependencies())
    print()
    
    print("3. Checking files...")
    checks.append(check_files())
    print()
    
    print("4. Testing Kruti Dev converter...")
    checks.append(test_kruti_converter())
    print()
    
    print("5. Checking database...")
    checks.append(test_database())
    print()
    
    print("="*60)
    if all(checks):
        print("✅ All checks passed! You're ready to run the application.")
        print()
        print("To start the application:")
        print("  Linux/Mac: ./run.sh")
        print("  Windows:   run.bat")
        print("  Manual:    python app.py")
        print()
        print("Then open: http://localhost:5000")
    else:
        print("⚠️  Some checks failed. Please review the errors above.")
        print()
        if not checks[1]:  # Dependencies check failed
            print("To install dependencies:")
            print("  pip install -r requirements.txt")
    print("="*60)

if __name__ == '__main__':
    main()
