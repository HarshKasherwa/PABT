import json

import requests
from starlette.responses import HTMLResponse
from fastapi import APIRouter, HTTPException
import wikipediaapi
import wikipedia
from bs4 import BeautifulSoup

router = APIRouter()

project_name = "PABT"
user = "kasherwa.h@gmail.com"
user_agent = f"{project_name} ({user})"

headers = {
    'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJmMzhhYjhkNjcyNDFkZWMwOGQ5YTZjNGI3ODQ4MTNkMyIsImp0aSI6IjA1N2ZmMWFlMDZjNTkyNjFhYjdhZTQ0MjQ1YjdjM2ZlZjhjNWZkZGZkYzI2NGY5NjE4ZjE3ZjAyMmY2OTVmODA5YjcwNzc5MzhjMTU2ZDhiIiwiaWF0IjoxNzMyOTc5MDM5LjEyNDI0MSwibmJmIjoxNzMyOTc5MDM5LjEyNDI0NCwiZXhwIjozMzI4OTg4NzgzOS4xMjI2LCJzdWIiOiI3NzA3MjU3MyIsImlzcyI6Imh0dHBzOi8vbWV0YS53aWtpbWVkaWEub3JnIiwicmF0ZWxpbWl0Ijp7InJlcXVlc3RzX3Blcl91bml0Ijo1MDAwLCJ1bml0IjoiSE9VUiJ9LCJzY29wZXMiOlsiYmFzaWMiXX0.TnJuQ8E2rknHH0UmN1b_Powvb8ecQSM_Mhf7OYUjj8XV5WyQmbge4zb2rLPAxdohNYYE2GQWCi7wVU8mX1myRxwc_JWBMpsMZXi3p2QqGDrbsc525L4NZqDDPZK4FXsdoPiioZKeQTFNI1MF5YhfTYUHvj2TtO_qu1s-_ioWHzFSwCtOhywfzodBWwuf9NDnuJZzzBw6_35vCBVL5peIM3h1Zkxb7bjnfztdI6QH-gqXU8siCZrcMTr59Q534qz2xCrR2h_K5rz_0rmJtIeGOb2jQ-ezoXV7lJVuiPCfhZ7iy7SNz55fwuiVW4Do2OP9MgNqm2tg_l3zu41pSpeDNDV6SmnWJ4zk0UACp7d3Cx4B4RDE_Mq2c2ckTbA0f9VvVmwITp2pTjUDpJo_z81t5bTuTzKLOyQIxXfaKKNbhOCE1AwQpXRcxjBjWUlt1y-RZQLH-MN86SRzjRDPO7WEifSO-g71gdtKa8gOY6My9nugf7aeG3A6LIKponC7G1CTYBsyhRptvuewQFbMlzt2jmztLKO1Gsy79kuaUEqS16iyKWxIIJJ1HLW6qqsH5KZiinEHFCvn8KUK24ii0pjqHUA75mPcsrBUa584JTRQX9AsaWy46gb4Uhr_gpiXU1Je-RhcVN63Kgq4B4Bzbx_Cc0kHofUap58qN579XU6kxkk',
    'User-Agent': user_agent
}
base_url = 'https://api.wikimedia.org/core/v1/wikipedia/'
language_code = 'en'

@router.get("/search")
async def search_wikipedia(keyword: str):
    search_results = wikipedia.search(keyword)
    # wiki_wiki = wikipediaapi.Wikipedia(
    #     user_agent="YOUR_APP_NAME (YOUR_EMAIL_OR_CONTACT_PAGE)",
    #     language='en',
    # )
    # search_results = wiki_wiki.(keyword)
    print(f"type: {type(search_results)}")
    # print(f"search_results: {search_results}")
    print(search_results)
    try:
        # return {"articles": search_results}
        return search_results
    except Exception as e:
        return HTTPException(status_code=404, detail="Article not found")

@router.get("/search2")
async def search_wikipedia2(keyword: str):
    search_query = keyword
    number_of_results = 10
    endpoint = '/search/page'
    url = base_url + language_code + endpoint
    parameters = {'q': search_query, 'limit': number_of_results}
    response = requests.get(url, headers=headers, params=parameters)
    return response.json()


def get_full_wiki_page(title):
    wiki_wiki = wikipediaapi.Wikipedia(
        user_agent=user_agent,
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )
    page_py = wiki_wiki.page(title)
    if page_py.exists():
        return page_py.text
    else:
        return None

@router.get("/get_page")
async def get_page(title: str):
    content = get_full_wiki_page(title)
    if content:
        return HTMLResponse(content=content)
    else:
        return HTMLResponse(content="<h1>Page not found</h1>", status_code=404)


@router.get("/get_page_desc")
async def get_page_desc(title: str):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'parse',
        'format': 'json',
        'page': title,  # The page title from the URL
        'prop': 'text',
        'redirects': True,
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

@router.post("/save")
async def save_article(article: dict):
    # Implement save logic
    pass