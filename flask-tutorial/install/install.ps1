cd flask-tutorial\install
pip install -r requirements.txt
cd..
$env:FLASK_APP = "flaskr"
$env:FLASK_ENV = "development"
python -m flask init-db