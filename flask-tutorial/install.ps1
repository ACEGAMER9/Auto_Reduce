cd flask-tutorial
pip install -r requirements.txt
python3 -m venv venv
$env:FLASK_APP = "flaskr"
$env:FLASK_ENV = "development"
python -m flask init-db
[system.Diagnostics.Process]::Start("chrome","http://127.0.0.1:5000")
python -m flask run