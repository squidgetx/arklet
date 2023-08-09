default: local

local:
	docker-compose up --build

prod: redeploy webserver

redeploy: 
	git pull
	docker-compose -f docker-compose.nginx.yml up --build --detach --profile arklet

webserver:
	docker-compose -f docker-compose.nginx.yml down -v nginx
	docker-compose -f docker-compose.nginx.yml up --build --detach
	sleep 2
	docker exec -it arklet-frick-nginx-1 /ssl_setup.sh

dev-cmd:
	docker exec -it arklet_minter /bin/bash

dev-psql:
	source docker/env.local && docker exec -it arklet_db psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB"
