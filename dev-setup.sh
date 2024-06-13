source .venv/bin/activate
pip install -e .
pre-commit install -t pre-commit -t commit-msg
