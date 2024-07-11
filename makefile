restart-api:
	docker compose stop apiserver; docker compose up -d --no-deps --force-recreate apiserver

restart-web:
	docker compose stop webserver; docker compose up -d --no-deps --force-recreate webserver

restart-file:
	docker compose stop fileserver; docker compose up -d --no-deps --force-recreate fileserver

re:
	docker compose down; docker compose up -d

DOMAIN ?= 8000-$${LIGHTNING_CLOUDSPACE_HOST}

replace:
	sed -i "s/mydomain\.com/$(DOMAIN)/g" nginx.conf
