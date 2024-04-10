export DOTENV_FILE=.env_gaz
alembic upgrade head
uvicorn node.app:app --port 7890