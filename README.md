TO-DO (Django)

A simple, clean Todo web app built with Django and Tailwind (CDN). Add tasks with due dates and priorities, mark them done/undo, and delete—all in a responsive UI with a friendly green palette.

Repo contains a Django project (todo) and app (tasks) alongside manage.py and db.sqlite3. 
GitHub

✨ Features

Add tasks with title, optional due date, and priority (High/Medium/Low)

Done/Undo toggle and Delete

Responsive, card-style task UI with header & footer

Color palette used:

#328E6E, #67AE6E, #90C67C, #E1EEBC

🧱 Tech Stack

Python / Django

HTML + Tailwind (CDN)

Languages in this repository: Python ~53%, HTML ~47% (as reported by GitHub). 
GitHub

📁 Project Structure (high level)
TO-DO/
├─ manage.py
├─ db.sqlite3
├─ todo/        # Project settings & URLs
└─ tasks/       # App: models, views, templates, static


Route names referenced by the templates include toggle_task and delete_task for Done/Undo and Delete actions.

🚀 Quick Start
1) Clone
git clone https://github.com/Rahat532/TO-DO.git
cd TO-DO

2) Create a virtualenv (recommended)
# macOS/Linux
python3 -m venv .venv && source .venv/bin/activate

# Windows (PowerShell)
py -m venv .venv
.venv\Scripts\Activate.ps1

3) Install dependencies

This project primarily needs Django (Tailwind is via CDN).

pip install --upgrade pip
pip install django
# On Windows you may also need:
pip install tzdata

4) Run migrations & start the server
python manage.py migrate
python manage.py runserver


Open: http://127.0.0.1:8000/

5) (Optional) Create an admin user
python manage.py createsuperuser
# then visit http://127.0.0.1:8000/admin/

🎨 UI Notes

Task items render as cards; completed tasks get a subtle completed style.

Priority badges:

High → #328E6E

Medium → #67AE6E

Low → #90C67C

Completed background hint uses #E1EEBC.

🧭 How to Use

Enter a task title (required).

(Optional) Set a due date.

Choose priority (defaults to Medium).

Click Add Task.

Use Done/Undo to toggle completion, or Delete to remove.

🧪 Tests

No automated tests yet. PRs adding unit tests (e.g., pytest/pytest-django) are welcome.

📦 Deployment Tips

Minimal static handling needed since Tailwind is loaded via CDN.

For production, consider:

Setting DEBUG = False, ALLOWED_HOSTS

Adding a real database (e.g., PostgreSQL) and environment config

Using a process manager (Gunicorn/Uvicorn) behind Nginx on a host like Render/Railway

🤝 Contributing

Issues and PRs are welcome! Please:

Keep commits scoped and clear

Use descriptive PR titles and screenshots for UI changes

📜 License

No license file is currently included.

📸 Screenshots
<img width="1913" height="907" alt="image" src="https://github.com/user-attachments/assets/17068a2b-5881-4023-a3c0-9b952431768e" />
