export DOTENV_FILE=.env_sber
alembic upgrade head
uvicorn node.app:app --port 3456