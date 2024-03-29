install: 
	venv/bin/pip3 install --upgrade -r requirements.txt
	venv/bin/pip3 install -e .

venv:
	pip3 install --user virtualenv
	python3 -m virtualenv venv

flake8:
	venv/bin/flake8

control: 
	venv/bin/python3 -i control.py

screen: 
	watch -n 0.1 venv/bin/python3 screens.py

scanner: 
	watch -n 1 venv/bin/python3 scanner.py
