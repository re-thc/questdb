# QUEST

## Assumptions 
- there is a running kubernetes cluster somewhere called <cluster> and a kubeconfig file has been setup on this Python client.
- use a real database in production instead of a dictionary
- only very basic error handling is provided
- uses the default namespace
- Requires Python 3.7+
- Requires kubernetes cluster 1.23 +-
- `questdb_*.yml` was extracted from QuestDB's public helm chart by running the command `helm install questdb questdb/questdb --dry-run --debug` to ensure best practices are followed

## Setup

1. Install Python and PIP
2. pip install -r requirements.txt

## Run

1. `uvicorn main:app` or `uvicorn main:app --reload` for dev and this runs on http://127.0.0.1:8000
2. GET `http://127.0.0.1:8000/questdb/<instance_id>` returns the status of the instance with `id`
3. DELETE `http://127.0.0.1:8000/questdb/<instance_id>` deletes the instance with `id`
4. POST `http://127.0.0.1:8000/questdb` creates a questdb instance and returns the `id`

## Test

pytest