from typing import List

from fastapi import APIRouter

from app.langchain_gemini import auto_generate_tags
from app.wikipedia import get_full_wiki_page

tagger_router = APIRouter()

@tagger_router.get(
    path="/tagger/generate_tags",
    tags=["Tagger"],
)
def generate_tags(
        article_title: str,
        no_of_tags: int = 7,
):
    print("API HIT")
    # article: str = await get_page("Earth")
    article = get_full_wiki_page(title=article_title)
    tags: List = auto_generate_tags(article, no_of_tags)
    return {"tags": tags}