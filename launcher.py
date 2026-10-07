import os
import sys
import time
import shutil
import subprocess
import webbrowser

# JEEVAN-ALERT project folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

APP_FILE = os.path.join(BASE_DIR, "app.py")

PORT = "8503"

# Find Python
python_exe = shutil.which("python")

if python_exe is None:
    python_exe = shutil.which("py")

if python_exe is None:
    raise RuntimeError("Python is not installed or not available in PATH.")

# Start Streamlit
process = subprocess.Popen(
    [
        python_exe,
        "-m",
        "streamlit",
        "run",
        APP_FILE,
        "--server.port",
        PORT,
        "--server.headless",
        "true"
    ],
    cwd=BASE_DIR,
    creationflags=subprocess.CREATE_NO_WINDOW
)

# Give Streamlit some time to start
time.sleep(4)

# Open browser
webbrowser.open(f"http://localhost:{PORT}")

# Keep launcher alive while Streamlit is running
process.wait()