cd flask-tutorial
$env:FLASK_APP = "flaskr"
$env:FLASK_ENV = "development"
[system.Diagnostics.Process]::Start("chrome","http://127.0.0.1:5000")
python -m flask run