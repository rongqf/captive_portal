## help - to display this help
.PHONY: help
help: Makefile
	@sed -n 's/^##//p' $<


## dev - run dev server
.PHONY: dev
dev:
	cd src && uv run python main.py run-server && cd ..


## tree - build project tree
.PHONY: tree
tree:
	tree -v -I "*.pyc|__init__.py|__pycache__" -L 3

## deploy - run ansible-playbook for deploying to target, `env SLUG=thsz make deploy`
SLUG?=stage
.PHONY: deploy
deploy:
	cd deploy \
	&& \
	ansible-playbook \
	-i hosts.ini \
	playbook.yml \
	-e @slug_$(SLUG).vars.yml \
	-e @base.vars.yml \
	-e @slug_$(SLUG).vars.yml \
	-u ubuntu \
	-b \
	${ARGS} \
	;

## lint - lint source files
.PHONY: lint
lint:
	isort .
	black .
	flake8 .
	bandit -r .
	mypy .

## test - run project test
.PHONY: test
test:
	pytest --junitxml=junit.xml --cov=. tests
	coverage xml
	coverage html


## requirements - export requirements.txt
.PHONY: requirements
requirements:
	uv pip freeze > src/requirements.txt

## clean - clean build and test files
.PHONY: clean
clean:
	rm -rvf htmlcov
	rm -rfv dist
	rm -rfv build

## shiv - build pyz execute
.PHONY: shiv
shiv: clean
	mkdir -p build
	poetry install
	cp -r src dist
	poetry run \
		pip install -r src/requirements.txt --target dist/
	poetry run \
		shiv \
		--site-packages dist \
		--compressed \
		--reproducible \
		--compile-pyc \
		-p '/usr/bin/env python3.9' \
		-o build/$(shell basename $(shell realpath .)).pyz \
		;
	ls -l build/

## bumpversion - bump version and then push with tags
.PHONY: bumpversion
bumpversion:
	git pull
	poetry run bumpversion patch
	git push
	git push --tags
