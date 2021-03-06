# Banxico Outstanding Debt App

## Hosted Demo

http://banxico.atompaper.com

![Demo](/demo.png)

## Setting up a Python environment to run scripts

Library dependencies are listed in requirements.txt.

```bash
python3.6 -m venv venv;
pip install --upgrade pip;
pip install -r requirements.txt;
source venv/bin/activate; # or Windows equivalent
```

## Running the UI locally

The UI is a Plotly/Dash app. With the venv properly activated, run:

```bash
python application.py
```

## Running the Crawler locally

The crawler script updates the ./db directory with the results of the latest run. With the venv properly activated, run:

```bash
python crawler.py
```

## Running unittest

With the venv properly activated, run:

```bash
nosetests
```
