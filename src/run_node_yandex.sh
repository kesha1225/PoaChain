export DOTENV_FILE=.env_ya
alembic upgrade head
uvicorn node.app:app --port 1234