default: local

local:
	docker-compose up --build

prod: webserver

redeploy: 
	git pull
	docker-compose -f docker-compose.nginx.yml up --build --detach
	docker-compose -f docker-compose.nginx.yml --profile nginx restart nginx

webserver:
	docker-compose -f docker-compose.nginx.yml --profile nginx up --build --detach
	sleep 2
	docker exec -it arklet-frick-nginx-1 /ssl_setup.sh

dev-cmd:
	docker exec -it arklet_minter /bin/bash

dev-psql:
	source docker/env.local && docker exec -it arklet_db psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB"
