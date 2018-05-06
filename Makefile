setup:
	python3 -m venv ~/.pragai

install:
	pip install -r requirements.txt

test:
	cd chapter7; py.test --nbval-lax notebooks/*.ipynb

lint:
	pylint --disable=W,R,C *.py

lint-warnings:
	pylint --disable=R,C *.py
