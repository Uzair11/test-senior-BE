setup:
	@make build
	@make upd 

down:
	docker-compose down

down-volumes:
	docker-compose down -v 

stop:
	docker-compose stop

up:
	docker-compose up

upd:
	docker-compose up -d

status:
	docker-compose ps -a

build:
	docker-compose build --no-cache --force-rm

console:
	docker exec -it test-flask-app /bin/bash

start: 
	docker exec -it test-flask-app flask --app app run --host=0.0.0.0 --debug 

restart:
	@make down
	@make upd