.PHONY: update

# Docker services
DOCKER_COMPOSE_PROJECT_NAME=exercise_manager_bot_services_local
LOCAL_DOCKER_COMPOSE_FILE=./docker/local/docker-compose.yml

up_local_services:
	docker compose -p $(DOCKER_COMPOSE_PROJECT_NAME) -f $(LOCAL_DOCKER_COMPOSE_FILE) up -d

down_local_services:
	docker compose -p $(DOCKER_COMPOSE_PROJECT_NAME) -f $(LOCAL_DOCKER_COMPOSE_FILE) down

restart_local_services: down_local_services up_local_services

local_services_logs:
	docker compose -p $(DOCKER_COMPOSE_PROJECT_NAME) -f $(LOCAL_DOCKER_COMPOSE_FILE) logs

# Localization
DEFAULT_LOCALES_DIR=locales

compile_locales:
	python scripts/compile_locales.py $(or $(LOCALES_DIR), $(DEFAULT_LOCALES_DIR))

# Deployment
DEFAULT_SERVICE_NAME = exercise_manager_tg_bot

get_updates:
	git pull
	sudo systemctl restart $(or $(SERVICE_NAME), $(DEFAULT_SERVICE_NAME))
	sudo systemctl --no-pager status $(or $(SERVICE_NAME), $(DEFAULT_SERVICE_NAME))
