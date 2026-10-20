# Django + ChatterBot Terminal Chatbot

A class project demonstrating a command-line chatbot using Django management commands and the ChatterBot Python library.

## Requirements

- Python 3.11 (recommended)
- Internet connection for the first package installation

## Setup (Windows PowerShell)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m spacy download en_core_web_sm
python manage.py check
python manage.py chatbot
```

For macOS/Linux, activate the environment using `source .venv/bin/activate`.

## Usage

Type a message after `user:` and the bot prints its reply after `bot:`. Type `exit` or `quit` to close the session. Example phrases: `Hello`, `What is Django?`, and `What is your name?`.

Training runs each time by default. After your first successful run, use `python manage.py chatbot --skip-training` to reuse saved training data.

## Files

- `chat/bot_service.py`: chatbot creation, training data, and response function
- `chat/management/commands/chatbot.py`: terminal UI with Django's management command framework
- `chatbot_project/settings.py`: minimal Django configuration
- `requirements.txt`: third-party Python dependencies (assignment manifest)
- `manage.py`: Django command runner

## Notes

- Responses depend on the available training examples and may differ from the examples shown in an assignment.
- `chatterbot.sqlite3` is created locally when running the chatbot and excluded from Git.
- The Django project exists to run the terminal command; a web server is not required.
- This is an educational example, not a general-purpose language model.

## Submission

1. Test the program locally and capture a screenshot of your **actual terminal output**.
2. Upload the source files, `README.md`, `requirements.txt`, and `.gitignore` to your own GitHub repository; omit `.venv/` and database files.
3. In a Word document, insert the screenshot, briefly explain the architecture, and add the repository URL.
