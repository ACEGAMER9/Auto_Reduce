cd flask-tutorial
pip install -r requirements.txt
$env:FLASK_APP = "flaskr"
$env:FLASK_ENV = "development"
python -m flask init-db