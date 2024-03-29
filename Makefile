DOCKER_UP := docker-compose up -d

collectstatic:
	python manage.py collectstatic -c

migrate:
	python manage.py compilemessages
	python manage.py makemigrations && python manage.py migrate

docker-up:
	$(DOCKER_UP)

webless:
	$(DOCKER_UP) db thumbor memcached

clear-silk:
	python manage.py silk_clear_request_log