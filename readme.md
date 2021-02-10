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
pip install -r requirements.txt
python run.py
```

# Bot configuration

You may configure some properties in bot/app/config.py