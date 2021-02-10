# Run database for project local development

```{bash}
docker run -d \
	--name network \
	-e POSTGRES_USER=postgres \
	-e POSTGRES_PASSWORD=postgres \
	-e POSTGRES_DB=network \
	-p 5430:5432 \
	postgres

```


# Run website via Docker contatiners

```{bash}
docker-compose up --build -d
```


# Run bot

```{bash}
cd ./bot
python3 -m venv env
source env/bin/activate
python run.py
```

# Bot configuration

You may configure some propertities in bot/app/config.py