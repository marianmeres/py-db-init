# db-init.py

Python study playground, doing some real work.

## Installation

Make sure you have python 3.6+ available on your system.

1. `pip install -r requirements.txt`
2. `cp .env.example.env .env`
3. `vim .env` (edit db credentials as needed)
4. `python3 db-init.py --help` 

## Usage

```
usage: db-init.py [-h] --indir INDIR [--env ENV] [--force] [--yes] [--silent] [--dry]

Utility to collect and execute sql files from a given directory. 

Execution of files is sorted based on their declared dependency via magic sql comment: 
-- ## require <filename>

optional arguments:
  -h, --help     show this help message and exit
  --indir INDIR  Source directory containing sql files. Multiple --indir args are allowed.
  --env ENV      Optional path to .env file (default: ./.env)
  --force        Will run even on production env (detected via PYTHON_ENV)
  --yes          Do not ask for confirmation and assume "yes"
  --silent       Do not produce stdout output
  --dry          Just return collected sql, but do not execute it against db
```

## Example

```
python db-init.py --indir data/db-schema/

python db-init.py --indir data/db-schema/ --indir data/db-data/ --yes 
```
