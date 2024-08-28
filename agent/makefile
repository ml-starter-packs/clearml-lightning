up: .env
	docker build -t worker .
	docker compose up -d
	sleep 3 && docker logs worker001

down:
	docker compose down

re: down up

kill:
	docker ps -a | tail -n+2 | awk '{print $$1}' | xargs docker rm -f

chaos:
	ps aux | grep "ssh -N" | grep -v grep | awk '{ print $$2 }' | sudo xargs kill -9

logs:
	docker logs -f worker01

.env: .env.template
	@echo "Creating \`.env\` and populating secrets"
	@cp .env.template .env
	# @python3 -c 'import secrets; print(f"CLEARML_API_ACCESS_KEY={secrets.token_hex(16)}\nCLEARML_API_SECRET_KEY={secrets.token_hex(32)}")' >> .env
