# Quotes Scraper API

A service for scraping quotes from [Quotes To Scrape](https://quotes.toscrape.com/) using FastAPI, Celery, Redis, and MongoDB.

## Getting Started

Follow these steps to set up and run the application.

### 1. Clone the Repository

First, clone the project from GitHub to your local machine:

```bash
mkdir your_folder
cd your_folder
git clone https://github.com/AlexanderBeli/TestWork01.git
```

### 2. Run Docker Compose

```bash
cd TestWork01
docker compose up --build       # You will see all logs in the terminal
docker compose up --build -d    # In this case you can see logs in Docker Desktop
```

### 3. Open the browser

- Open `http://0.0.0.0:8000/docs` or `http://0.0.0.0:8000` and play with endpoints.
- You can open `http://localhost:5555/tasks` and see the tasks report.

### 4. Stop Docker Compose

```bash
`ctr`+`C`               # if you run by docker compose up --build
docker compose down     # if you run by docker compose up --build -d
```

## Tests

For local testing you can install libraries from `requirements.txt` using .venv and then run `pytest`.

```bash
virtualenv .venv -p python3.13
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

## License

MIT License
