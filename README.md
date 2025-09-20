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

## Recent fixes & developer notes

- Flash messages: templates now render only the latest flash message (so users see one clear alert such as "Task added." or "Welcome back, <username>!"). Alerts are dismissible and auto-hide after a few seconds. If you want a shared include for this snippet I can extract it to `templates/includes/messages.html`.

- Login welcome message: a friendly "Welcome back, <username>!" message is added on successful login by `RoleAwareLoginView`.

- Profile header: profile pages (detail + edit) display a Home link in the header that routes admins to `accounts:dashboard` and regular users to `tasks:task_list`.

- Message rendering bug fixed: templates previously used `messages|last` which caused a TypeError with Django's message storage; they now use a safe `for m in messages` loop and render only the final item.

## How to test the message flows

1. Start the development server

```bash
python manage.py runserver
```

2. Sign up a new user (or use existing user) and log in. You should see a welcome message on the first redirect:

- Admins: redirected to `accounts:dashboard` with a "Welcome back, <username>!" alert.
- Regular users: redirected to the task list with the same welcome alert.

3. Create a task from the task list. You should see a single "Task added." message that disappears after ~5s (or when dismissed).

4. Delete a task: you should see "Task deleted." as a single alert.

If you observe multiple stacked alerts or a lingering message across pages, restart the server and try again — the message storage should be consumed after rendering the template.

## Dev checklist / next steps

- Consider extracting the flash-message HTML/JS into a shared include for DRYness.
- Add tests for message flows and for-permissions on task operations (task creation/update/delete must be owner-only).
- Add brief CONTRIBUTING.md and LICENSE if this project will be shared publicly.

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
FOR ADMIN
<img width="1918" height="916" alt="image" src="https://github.com/user-attachments/assets/941d20c1-100d-48a9-a8c0-ef19d7955a08" />
<img width="1917" height="908" alt="image" src="https://github.com/user-attachments/assets/4aed8bfd-52cd-4908-b40c-9e1ce4c9615f" />
<img width="1918" height="732" alt="image" src="https://github.com/user-attachments/assets/419c76b6-5301-4d3e-81e1-cd6c90bd0e21" />
<img width="1918" height="825" alt="image" src="https://github.com/user-attachments/assets/13dac825-0567-4aa4-b18f-c074b4610e20" />
<img width="1906" height="888" alt="image" src="https://github.com/user-attachments/assets/91e3a34e-61ab-45f8-8efe-438c431ad0ae" />
<img width="1671" height="788" alt="image" src="https://github.com/user-attachments/assets/bdbc40de-ddd9-45e5-9e1c-1e0a49acae90" />
<img width="1917" height="807" alt="image" src="https://github.com/user-attachments/assets/aa255abe-5385-48af-8f6f-16852846a82b" />
<img width="1918" height="796" alt="image" src="https://github.com/user-attachments/assets/d365fd4a-7f4f-41a9-b00d-6ccab5605883" />
<img width="1916" height="853" alt="image" src="https://github.com/user-attachments/assets/e86dacb0-7c74-465a-97fe-c578edfb2eb3" />









