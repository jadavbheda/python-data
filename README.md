# python-data

----
# Housekeeping

lint:
	black . --line-length=120

clean:
	find . -name '*.pyc' -delete

# Local Development

build:
	docker-compose build python-data

run:
	docker-compose run --service-ports python-data

shell:
	docker-compose run --service-ports python-data bash

# Local Validation

build-validate:
	docker-compose build validate

test:
	docker-compose run validate pytest

flake:
	docker-compose run validate flake8

type-check:
	docker-compose run validate mypy ./app

vulnerability-check:
	docker-compose run validate safety check
----


## Running

Enter the container and run:

    python app/main.py

## Local Development

Clone this repo, then build the image and enter a shell in that image:

    make run

### Validation Steps

#### Running tests

Enter the container and run:

    make test

#### Running type validation

Enter the container and run:

    make type-check

#### Running vulnerability checks

Enter the container and run:

    make vulnerability-check

#### Other info
- Project template using cookie cutter teamplate : https://github.com/macleodmac/cookiecutter-python-docker