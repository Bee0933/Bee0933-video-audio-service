install:
	# install dependencies
	pip install --upgrade pip &&\
		pip install -r requirements.txt 
format:
	# format python code with black
	black *.py  db/*.py
lint:
	# check code syntaxes
	pylint --disable=R,C *.py db/*.py

create_postgres:
	# create postgres docker db
	docker run -it \
		-e POSTGRES_USER="root" \
		-e POSTGRES_PASSWORD="root" \
		-e POSTGRES_DB="auth" \
		-v $(pwd)/auth_db:/var/lib/postgresql/data \
		-p 5433:5432 \
		postgres:13

create_user:
	# create user tables from ORM local test
	python3 db_cli.py create

populate_user_db:
	# create dummy data for user db
	python3 db_cli.py populate 'best@mail.com' 'pass'


all: install format lint 