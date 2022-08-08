cd ..\SmartFarm
$env:FLASK_APP = "App"
$env:FLASK_ENV = "development"
[system.Diagnostics.Process]::Start("chrome","http://127.0.0.1:5000")
python -m flask run