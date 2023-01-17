install:
	# install dependencies
	pip install --upgrade pip &&\
		pip install -r requirements.txt 
format:
	# format python code with black
	black *.py  auth/*.py auth_svc/*.py storage/*.py
lint:
	# check code syntaxes
	pylint --disable=R,C *.py auth/*.py auth_svc/*.py storage/*.py
	


all: install format lint 