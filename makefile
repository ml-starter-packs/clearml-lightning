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
	sudo rm -rf ~/opt
