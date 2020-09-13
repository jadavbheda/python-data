# python-data


## Local Development

Clone this repo, then build the image and enter a shell in that image:

    
    make build
    make run
    
    make shell (# access container shell)
    
    # From container shell: to run manually
    cd /opt/app
    python main.py
    

### Validation Steps

    make build-validate
    
	docker-compose build validate

    make test # (run py-test)	

    make flake # flake-8 validator

#### Running tests

Enter the container and run:

    make test

#### Running type validation

Enter the container and run:

    make type-check


#### Other info
- Project template using cookie cutter teamplate : https://github.com/macleodmac/cookiecutter-python-docker