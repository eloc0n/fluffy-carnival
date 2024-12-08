import json
import aiohttp
import httpx
from aiohttp import ClientError

from schemas.schemas import University

url = "http://universities.hipolabs.com/search"


def get_all_universities_for_country(country: str) -> dict:
    params = {"country": country}
    client = httpx.Client()
    response = client.get(url, params=params)
    response_json = json.loads(response.text)
    universities = []
    for university in response_json:
        university_obj = University.model_validate(university)
        universities.append(university_obj.model_dump_json())
    return {country: universities}


async def fetch_university_data(url: str, country: str) -> list:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                url, params={"country": country}, timeout=10
            ) as response:
                if response.status != 200:
                    raise ClientError(f"HTTP Error: {response.status}")
                return await response.json()
        except ClientError as e:
            print(f"Error fetching data for {country}: {e}")
            raise
