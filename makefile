default: prod

prod: 
	docker-compose -f docker-compose.prod.yml up 

dev-cmd:
	docker exec -it arklet_minter /bin/bash

dev-psql:
	source docker/env.postgres.local && docker exec -it arklet_db psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB"