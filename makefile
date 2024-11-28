# Check id docker-compose is available else use docker compose
ifeq (, $(shell which docker-compose))
    DC = docker compose
else
    DC = docker-compose
endif
UID = $(shell id -u)


# Format python files.
format:
	${DC} run --no-deps --user ${UID} fastapi bash -c "ruff check --fix . && ruff format ."

# Build docker images.
build:
	${DC} build --pull

# Start project.
start:
	${DC} up --remove-orphans

# Run tests.
test:
	${DC} ...

# Exec bash shell on fastapi container.
shell:
	${DC} run --user ${UID} --rm fastapi bash