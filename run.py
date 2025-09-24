#!/usr/bin/env python3
"""
Sylverith School Management System - Flask Application Runner
"""

import os
import sys
from app import app

if __name__ == '__main__':
    print("=" * 60)
    print("🎓 SYLVERITH SCHOOL MANAGEMENT SYSTEM")
    print("=" * 60)
    print("🚀 Starting Flask application...")
    print("📱 Access the application at: http://localhost:5000")
    print("🔐 Test credentials:")
    print("   • admin@sylverith.com / admin123")
    print("   • principal@sylverith.com / principal123")
    print("   • registrar@sylverith.com / registrar123")
    print("=" * 60)
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Shutting down Sylverith...")
        sys.exit(0)
