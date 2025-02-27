# Statement Analysis
Analayze the statement using the description and extract useful information from them store them in DB. These stored information is used in FE to visualize the data.


## Run in Docker
Create and update the .env in the root folder

.env
```
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
REDIS_URL=redis://redis:6379/0
DATABASE_HOST=postgres
DATABASE_USER=postgres
DATABASE_NAME=statement-analysis
DATABASE_PASSWORD=password
```

Then run the command
```shell
docker compose up --build -d  
```
Server will run on the following URL http://localhost:8001

Access the available APIs from http://localhost:8001/docs


## Run locally
1. Install redis locally
2. Start the redis server
2. Create .env file and add the OpenAI API key in the varaible `OPENAI_API_KEY`

In .env file 

```
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
REDIS_URL=YOUR_REDIS_URL
DATABASE_HOST=YOUR_POSTGRES_DB_HOST_URL
DATABASE_USER=POSTGRES_DB_USER_NAME
DATABASE_NAME=statement-analysis
DATABASE_PASSWORD=YOUR_PASSWORD
```

**Create a python virtual environment.** 

Then run the following commands
```
$ make install
$ make dev
$ make worker
```

- `make install` will install the required dependecies
- `make dev` will run the fastapi dev server
- `make worker` will run the celery worker 

Then the server will run on the following URL http://locahost:8001
