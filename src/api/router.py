import json

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from cachetools import TTLCache
from datetime import datetime
from utils.scraper import RealtorScraper
from utils.common import flatten_dict

# Define a Pydantic model for the input URL
class URLInput(BaseModel):
    url: HttpUrl
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "url": "https://realtor.com/realestateandhomes-search/Los-Angeles_CA/type-single-family-home/price-na-600000/",
                }
            ]
        }
    }

# Initialize a TTL cache to store scraped data temporarily
cache = TTLCache(maxsize=100, ttl=3600)

# Create an APIRouter instance
realtor_router = APIRouter()

# Define a route to provide information about the API
@realtor_router.get("/")
async def realtor_home():
    """
    Home endpoint for the Realtor scraping API.

    Returns:
        dict: A simple message indicating to visit the documentation for scraping data from Realtor.
    """
    return {"Message": "Visit the documentation for scraping data from Realtor"}

# Define a route to scrape properties from a given URL
@realtor_router.post("/properties/")
async def get_properties(url_input: URLInput):
    """
    Scrape properties from a given URL.

    Args:
        url_input (URLInput): Input URL to scrape properties from.

    Returns:
        dict: Scraped properties and metadata.

    Raises:
        HTTPException: If an error occurs during scraping.
    """
    if "realtor.com" not in url_input.url.host:
        raise HTTPException(status_code=400, detail="Invalid URL. Must be from https://www.realtor.com/")
    # Ensure that the URL ends with "/"
    if not url_input.url.path.endswith("/"):
        url_input.url = f"{url_input.url}/"

    cached_result = cache.get(url_input.url)
    if cached_result:
        return cached_result

    try:
        scraper = RealtorScraper(url=url_input.url, filepath='test.json')
        scraper.initialize()
        result = scraper.scrape()

        properties = result[0]
        metadata = result[-1]

        print(f"Fetched {len(properties)} Properties")
        flatten_properties = [flatten_dict(d) for d in properties]
        response = metadata
        response['count'] = len(properties)
        response['request_url'] = url_input.url
        response["properties"] = flatten_properties

        cache[url_input.url] = response
        return response

    except KeyError as e:
        print(e)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

