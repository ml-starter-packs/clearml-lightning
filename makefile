restart-api:
	docker compose stop apiserver; docker compose up -d --no-deps --force-recreate apiserver

restart-web:
	docker compose stop webserver; docker compose up -d --no-deps --force-recreate webserver

restart-file:
	docker compose stop fileserver; docker compose up -d --no-deps --force-recreate fileserver

restart-elastic:
	docker compose stop elasticsearch; docker compose up -d --no-deps --force-recreate elasticsearch

up:
	docker compose up -d

down:
	docker compose down

re:
	docker compose down; docker compose up -d

chaos:
	ps aux | grep ssh | awk '{ print $$2 }' | sudo xargs kill -9

DOMAIN ?= 8000-$${LIGHTNING_CLOUDSPACE_HOST}

replace:
	sed -i "s/mydomain\.com/$(DOMAIN)/g" nginx.conf

fresh: down
	sudo rm -rf ~/opt ~/usr /opt/clearml/
	sudo mkdir -p /opt/clearml/
	sudo mkdir -p /opt/clearml/data/elastic_7
	sudo mkdir -p /opt/clearml/data/mongo_4/db
	sudo mkdir -p /opt/clearml/data/mongo_4/configdb
	sudo mkdir -p /opt/clearml/data/redis
	sudo mkdir -p /opt/clearml/logs
	sudo mkdir -p /opt/clearml/config
	sudo mkdir -p /opt/clearml/data/fileserver
	sudo chown -R $$(id -u):$$(id -g) /opt/clearml/
	@echo "\nCleaned everything up!"

status:
	@docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"

dev-tools:
	sudo apt update && sudo apt upgrade -y \
		&& sudo apt install -yqq \
		tmux htop lsof strace

restart-docker:
	sudo service docker restart

logs:
	docker logs -n 100 -f clearml-apiserver
