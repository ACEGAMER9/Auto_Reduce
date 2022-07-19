cd SmartFarm\install
pip install -r requirements.txt
cd..
$env:FLASK_APP = "App"
$env:FLASK_ENV = "development"
python -m flask init-db