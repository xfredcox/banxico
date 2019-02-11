# Banxico Outstanding Debt

## Hosted Demo

http://banxico.s3-website.eu-west-2.amazonaws.com/

Supported on Chrome and Firefox.

## Running the UI locally

Use the following commands to run UI locally:

``bash
git clone git@github.com:xfredcox/banxico.git
cd banxico
python3.6 -m http.server
``

The page will be available on http://127.0.0.1:8000.


## Setting up a Python environment to run scripts

Library dependencies are listed in requirements.txt.

``bash
python3.6 -m venv venv
pip install --upgrade pip
pip install -r requirements.txt
source venv/bin/activate  # or Windows equivalent
``

## Running the Crawler locally

The script that collects data from Banxico is crawler.py. With the venv properly activated, run:

``bash
python crawler.py
``

The crawler script updates the ./db directory with the results of the latest run.


## Running unittest locally

With the venv properly activated, run:

``bash
python test_crawler.py
``
