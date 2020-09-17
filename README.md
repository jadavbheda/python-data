# python-data

FWF to CSV converter using python, docker/docker-composer. 

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style

## Local Development

Clone this repo, then build the image and enter a shell in that image:

    
    make build
    make run
    
    make shell (# access container shell)
    
        # From container shell: to run manually
        > cd /opt/app
        > python main.py
    

### Validation Steps

    make build-validate
    
	docker-compose build validate

    make test # (runs pytest)	

    make flake # flake-8 validator
    
    make lint # black auto formatter (ideally should be in precommit hook)

#### Running tests

Enter the container and run:

    make build-validate  # build dev container
    make test            # run pytests in dev container

## What does it do?
   
   Assumptions: Not reading file names from command line args. Instead read/write files in to below paths

    - Read specs from `data/spec.json`
    - Generates Fix width file at `data/fwf.txt`
    - Generates CSV from FWF file at `data/converted.csv`
    
   Directory Structure:
    
    - app
         - data: generate/read FWF, and generates CSV in this dir
         - generator: FWF generator
         - parser: FWF parser and CSV generator
         - utils: helpers; `fw_config` -> reads spec.json and creates python config object
   

#### Other info
- Project template using cookie cutter teamplate : https://github.com/macleodmac/cookiecutter-python-docker