compose_up:
	docker-compose up -d --wait db && docker-compose up -d web
	# we have to wait for db start, because web dockerfile has migrations to apply
	# better practice would be to perform migrate in entrypoint script
compose_down:
	docker-compose down