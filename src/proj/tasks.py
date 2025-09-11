"""Celery Tasks."""

from datetime import datetime

import httpx
from bs4 import BeautifulSoup

from src.database.db import collection_name
from src.database.models import Quote
from src.logger import logging
from src.proj.celery import app

logger = logging.getLogger(__name__)


@app.task(name="start_parsing_task", bind=True)
def start_parsing_task(self):
    """Celery task to scrape quotes from a website and save them to MongoDB."""

    quotes_url = "http://quotes.toscrape.com/"
    quotes_count = 0
    page_number = 1

    with httpx.Client() as client:
        while True:
            try:
                url = f"{quotes_url}page/{page_number}/"
                logger.info(f"Scraping page {page_number}: {url}")

                response = client.get(url)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")
                quotes = soup.find_all("div", class_="quote")

                if not quotes:
                    logger.info("No more quotes found. Scraping complete.")
                    break

                for quote_element in quotes:
                    text = quote_element.find("span", class_="text").text.strip()
                    author = quote_element.find("small", class_="author").text.strip()
                    tags = [tag.text.strip() for tag in quote_element.find_all("a", class_="tag")]

                    quote_obj = Quote(quote=text, author=author, tags=tags, time_added=datetime.now())

                    collection_name.insert_one(quote_obj.model_dump())
                    quotes_count += 1
                    logger.debug(f"Saved quote: '{text[:50]}...' by {author}")

                page_number += 1
            except httpx.HTTPError as e:
                logger.error(f"HTTP request error with httpx: {e}")
                raise self.retry(exc=e, countdown=60)
            except Exception as e:
                logger.error(f"An error occurred during scraping on page {page_number}: {e}")
                raise self.retry(exc=e, countdown=60)

    logger.info(f"Finished scraping. Total quotes saved: {quotes_count}")
    return {"message": "Scraping completed", "quotes_saved": quotes_count}
