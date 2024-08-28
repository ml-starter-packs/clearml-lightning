up: .env
	docker compose up -d

down:
	docker compose down

re: status
	docker compose down; docker compose up -d
	sleep 3 && make status

restart-api:
	docker compose stop apiserver; docker compose up -d --no-deps --force-recreate apiserver

restart-web:
	docker compose stop webserver; docker compose up -d --no-deps --force-recreate webserver

restart-file:
	docker compose stop fileserver; docker compose up -d --no-deps --force-recreate fileserver

restart-elastic:
	docker compose stop elasticsearch; docker compose up -d --no-deps --force-recreate elasticsearch

chaos:
	ps aux | grep "sshd" | grep -v grep | awk '{ print $$2 }' | sudo xargs kill -9

DOMAIN ?= 8000-$${LIGHTNING_CLOUDSPACE_HOST}

replace:
	sed -i "s/mydomain\.com/$(DOMAIN)/g" nginx.conf

fresh: down
	sudo rm -rf ~/opt ~/usr /opt/clearml/
	sudo mkdir -p ~/opt/clearml/
	sudo mkdir -p ~/opt/clearml/data/elastic_7
	sudo mkdir -p ~/opt/clearml/data/mongo_4/db
	sudo mkdir -p ~/opt/clearml/data/mongo_4/configdb
	sudo mkdir -p ~/opt/clearml/data/redis
	sudo mkdir -p ~/opt/clearml/logs
	sudo mkdir -p ~/opt/clearml/config
	sudo mkdir -p ~/opt/clearml/data/fileserver
	sudo chown -R $$(id -u):$$(id -g) ~/opt/clearml/
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

host:
	@echo "Run the following:"
	@echo "\n\t TARGET_LIGHTNING_ID=$${LIGHTNING_CLOUD_SPACE_ID} connect\n"

example:
	cd examples/tasks && python demo-task.py
	cd examples/pipes && python pipe_add_step.py

keys:
	@python3 -c 'import secrets; print(f"CLEARML_AGENT_ACCESS_KEY={secrets.token_hex(16)}\nCLEARML_AGENT_SECRET_KEY={secrets.token_hex(32)}")'

.env: .env.template
	@echo "Creating \`.env\` and populating secrets"
	@cp .env.template .env
	@python3 -c 'import secrets; print(f"CLEARML_AGENT_ACCESS_KEY={secrets.token_hex(16)}\nCLEARML_AGENT_SECRET_KEY={secrets.token_hex(32)}")' >> .env
