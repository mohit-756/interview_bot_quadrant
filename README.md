# interview_bot_quadrant-main

Quick setup and run instructions (Windows PowerShell).

1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r interview_bot_quadrant-main\requirements.txt
```

3. Initialize DB (creates `database.db`):

```powershell
python -c "import sqlite3; conn=sqlite3.connect('database.db'); print('DB created:', conn); conn.close()"
```

4. Run the app:

```powershell
$env:FLASK_APP='interview_bot_quadrant_main.app'
python -m flask run
# or
python -m flask --app interview_bot_quadrant_main.app run
```

Notes:
- The Flask app module is `interview_bot_quadrant-main/interview_bot_quadrant-main/app.py` (project root uses folder `interview_bot_quadrant-main`).
- If you have a `venv` already inside the project, activate that instead of creating `.venv`.

Cleanup:
- To remove the old `interview_bot_quadrant` folder (if it still exists), run the provided `cleanup.ps1` script safely.
