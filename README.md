# SkillBridge — Student Placement Preparation Tracker

SkillBridge is a beginner-friendly web application for organizing placement preparation. It lets a student manage learning goals, track progress, and maintain a simple list of job applications.

## Features

- Add, update, and delete learning goals
- Categorize goals and mark them Pending, In Progress, or Completed
- Track company applications and their current status
- Dashboard statistics and preparation progress indicator
- SQLite database that is created automatically
- Responsive dashboard layout

## Tech stack

- Python
- Flask
- SQLite
- HTML and CSS
- Git and GitHub

## Run locally

### 1. Install Python

Install Python 3.10 or later. During installation on Windows, select **Add Python to PATH**.

### 2. Open the project

Open this folder in Visual Studio Code.

### 3. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt terminal and run:

```bat
.venv\Scripts\activate.bat
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Start the app

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser. Stop the server with `Ctrl+C`.

## Push to your GitHub account

1. Create a new **empty** repository on GitHub, for example `skillbridge-placement-tracker`.
2. Open the VS Code terminal in this project folder.
3. Run the following commands, replacing `YOUR_USERNAME` with your GitHub username:

```bash
git init
git add .
git commit -m "Build SkillBridge placement tracker"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/skillbridge-placement-tracker.git
git push -u origin main
```

If Git says your name or email is not configured, set the name and email associated with your GitHub account:

```bash
git config --global user.name "Your Name"
git config --global user.email "YOUR_GITHUB_EMAIL"
```

Then repeat the commit and push commands. Sign in through the browser if GitHub asks for authorization.

## Important notes

- The database file `skillbridge.db` is intentionally excluded from Git by `.gitignore`; the app creates it automatically when run.
- This is a learning/portfolio starter, not a production-ready service. It does not include user accounts or authentication.
- Use your own original improvements and be ready to explain the code during interviews.
