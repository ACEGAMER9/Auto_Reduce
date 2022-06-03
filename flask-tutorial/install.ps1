cd flask-tutorial
pip install -r requirements.txt
python3 -m venv venv
.\venv\Scripts\activate
$env:FLASK_APP = "flaskr"
$env:FLASK_ENV = "development"
[system.Diagnostics.Process]::Start("chrome","http://127.0.0.1:5000")
flask run