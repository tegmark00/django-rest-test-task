docker run -d \
	--name network \
	-e POSTGRES_USER=postgres \
	-e POSTGRES_PASSWORD=postgres \
	-e POSTGRES_DB=network \
	-p 5430:5432 \
	postgres