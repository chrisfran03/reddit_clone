To run this application you need Python, pip, and SQLite.

Clone the project.

git clone https://github.com/chrisfran03/reddit_clone.git

Setup a venv and use pip to install the following project dependencies.

pip install flask
pip install flask_login
pip install flask_sqlalchemy 
pip install passlib
pip install flask_wtf
pip install wtforms
pip install bcrypt







****Only if there is no database*****

If there is no database and their is an error "no such table"
type in the terminal:
$env:FLASK_APP = "reddit.py"
set FLASK_APP=reddit.py
flask cli create_db

*************************************






