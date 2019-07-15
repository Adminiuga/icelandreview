# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help
APP_NAME := eztv
TARGET := dev

setup-env: ## setup the virtual environment
	$(eval pyversion := $(shell egrep -o '([[:digit:]\.])+' .python-version))
	$(eval env_name := $(shell cat .python-version))
	pyenv virtualenv ${pyversion} ${env_name}

setup-requirements: ## install requirements for the project
	pip install -r requirements.txt
	pip install -r requirements_dev.txt

format: ## reformat the code
	black -t py37 -l 120 *.py

run: ## run the server locally
	FLASK_ENV=development python main.py

deploy: ## deploy with Zappa
	zappa deploy $(TARGET)

update: ## update the deployed Zappa build
	zappa update $(TARGET)
