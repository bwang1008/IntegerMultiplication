# IntegerMultiplication

Implementation of integer multiplication algorithms on Multi-Tape Turing Machines.


## Installation

First clone the repository:
```bash
git clone https://github.com/bwang1008/IntegerMultiplication.git
cd IntegerMultiplication
```

Then setup the Python virtual environment, which uses the `uv` package installer:
```bash
python3 -m venv .venv   # creates virtual environment in .venv folder
source .venv/bin/activate   # activate virtual environment
pip3 install uv
uv pip install -r requirements.txt  # install required packages using uv
```

To run the tests,
```bash
pytest --cov=integer_multiplication integer_multiplication/tests
```
