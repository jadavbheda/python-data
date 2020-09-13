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