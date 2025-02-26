# Statement Analysis
Analayze the statement using the description and extract useful information from them store them in DB. These stored information is used in FE to visualize the data.

## Run locally
1. Install redis locally
2. Start the redis server
2. Create .env file and add the OpenAI API key in the varaible `OPENAI_API_KEY`

$ make install
$ make migrate
$ make run