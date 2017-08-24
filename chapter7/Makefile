#listing 7.1
setup:
	python3 -m venv ~/.pragai7

install:
	pip install -r requirements.txt

test:
	py.test --nbval notebooks/*.ipynb

lint:
	pylint --disable=W,R,C *.py

lint-warnings:
	pylint --disable=R,C *.py
