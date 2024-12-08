# Check id docker-compose is available else use docker compose
ifeq (, $(shell which docker-compose))
    DC = docker compose
else
    DC = docker-compose
endif
APP_NAME=fastapi
UID = $(shell id -u)


# Format python files.
format:
	${DC} up --remove-orphans --no-deps -d $(APP_NAME)
	${DC} exec --user ${UID} $(APP_NAME) bash -c "ruff check --fix . && ruff format ."

# Build docker images.
build:
	${DC} build --pull

# Start project.
start:
	${DC} up --remove-orphans

alembic-init:
	$(DC) run --rm --no-deps $(APP_NAME) bash -c "alembic init alembic"

alembic-revision:
	@read -p "Enter revision message: " msg; \
	$(DC) run --rm --no-deps $(APP_NAME) bash -c "alembic revision --autogenerate -m '$$msg'"

alembic-downgrade:
	@read -p "Enter downgrade revision: " msg; \
	$(DC) run --rm --no-deps $(APP_NAME) bash -c "alembic downgrade '$$msg'"

alembic-upgrade:
	$(DC) run --rm $(APP_NAME) bash -c "alembic upgrade head"

# Run the worker
worker:
	$(DC) run --rm $(APP_NAME) python service/consumer.py

# Run tests.
test:
	${DC} ...

# Exec bash shell on fastapi container.
shell:
	${DC} run --user ${UID} --rm $(APP_NAME) bash