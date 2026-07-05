"""
app.py
------
Main Flask application entry point.

For now this file only does the bare minimum needed to prove the stack
works end-to-end:
  1. Load environment variables from .env
  2. Create the Flask app
  3. Enable CORS so the React frontend (different port) can call the API
  4. Expose a single /api/health route that also checks the DB connection

Once this runs successfully (visit http://localhost:5000/api/health and
see {"status": "ok", "database": "connected"}), we will register the real
blueprints (auth, profile, quiz, ...) here one at a time, following the
build order in the design document.
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from config.db import test_connection

# Load variables from backend/.env into the environment
load_dotenv()

app = Flask(__name__)

# Allow the React dev server (e.g. http://localhost:5173) to call this API
CORS(app)


@app.route("/api/health", methods=["GET"])
def health_check():
    """
    Simple health check endpoint.

    Returns whether the Flask app is running AND whether it can
    successfully reach the MySQL database. This is the very first
    thing to test after setup - if this doesn't return "connected",
    nothing else (auth, quiz, roadmap, ...) will work either.
    """
    db_ok = test_connection()
    return jsonify({
        "status": "ok",
        "database": "connected" if db_ok else "unreachable"
    }), 200


# ----------------------------------------------------------------
# Blueprint registration (added incrementally as routes are built)
# ----------------------------------------------------------------
from routes.auth import auth_bp
app.register_blueprint(auth_bp, url_prefix="/api/auth")

from routes.profile import profile_bp
app.register_blueprint(profile_bp, url_prefix="/api")

from routes.academic_upload import academic_upload_bp
app.register_blueprint(academic_upload_bp, url_prefix="/api")

from routes.quiz import quiz_bp
app.register_blueprint(quiz_bp, url_prefix="/api")

from routes.grading import grading_bp
app.register_blueprint(grading_bp, url_prefix="/api")

from routes.skills import skills_bp
app.register_blueprint(skills_bp, url_prefix="/api")

from routes.roadmap import roadmap_bp
app.register_blueprint(roadmap_bp, url_prefix="/api")

from routes.progress import progress_bp
app.register_blueprint(progress_bp, url_prefix="/api")

from routes.career import career_bp
app.register_blueprint(career_bp, url_prefix="/api")

# All backend routes are now registered. Next: React frontend.


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "True") == "True"
    app.run(host="0.0.0.0", port=port, debug=debug)