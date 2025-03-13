run:
	python main.py

run3:
	python3 main.py

install-package:
	pip install -r requirements.txt

pyinstall:
	pip install $(PACKAGE) && pip freeze > requirements.txt
