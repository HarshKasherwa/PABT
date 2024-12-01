from typing import Optional, List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError, DatabaseError, NoResultFound

from auth.login import oauth2_scheme, get_current_user
from db.db_service_layer import ArticlesService, UsersService
from db.models import Articles

article_router = APIRouter()

@article_router.get(
    path="/crud_article/saved_articles_list",
    tags=["CRUD ARTICLE"]
)
def saved_articles_list(
        token: str = Depends(oauth2_scheme),
):
    user = get_current_user(token)
    userId = user["userId"]
    try:
        article_service_obj = ArticlesService()
        articles = article_service_obj.get_articles(filters={"userId": userId})
        resp = []
        for art in articles:
            art: Articles = art
            resp.append(art.title)
        return resp
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail="Articles not found")
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=f"DataBase Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Internal Server Error: {e}")

@article_router.post(
    path="/crud_article/save_article",
    tags=["CRUD ARTICLE"]
)
async def save_article(
        title: str,
        tags: Optional[List[str]] = None,
        token: str = Depends(oauth2_scheme),
):
    try:
        user = get_current_user(token)
        userId = user["userId"]
        if tags is None or tags == []:
            article_data = Articles(
                userId=userId,
                title=title
            )
        else:
            article_data = Articles(
                userId=userId,
                title=title,
                tags=tags
            )
        article_service_obj = ArticlesService()
        article_service_obj.insert_new_article(article=article_data)
        return {"message": "Article details saved successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid Input: {e}")
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=f"DataBase Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Internal Server Error: {e}")

@article_router.get(
    path="/crud_article/get_articles",
    tags=["CRUD ARTICLE"]
)
def get_articles(
        token: str = Depends(oauth2_scheme)
):
    try:
        username = get_current_user(token)
        username = username["username"]
        user_service_obj = UsersService()
        user = user_service_obj.get_user(filters={"username": username}, single_record=True)
        article_service_obj = ArticlesService()
        articles = article_service_obj.get_articles(filters={"userId": user.userId})
        return articles
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail="Articles not found")
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=f"DataBase Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Internal Server Error: {e}")

@article_router.get(
    path="/crud_article/get_article",
    tags=["CRUD ARTICLE"]
)
def get_article(
        articleId: int
):
    try:
        article_service_obj = ArticlesService()
        article = article_service_obj.get_articles(filters={"articleId": articleId}, single_record=True)
        return article
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail="Article not found")
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=f"DataBase Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Internal Server Error: {e}")

@article_router.delete(
    path="/crud_article/delete_article",
    tags=["CRUD ARTICLE"]
)
def delete_article(
        articleId: int
):
    try:
        article_service_obj = ArticlesService()
        article_service_obj.delete_article(articleId=articleId)
        return {"message": f"Article {articleId} deleted successfully"}
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail="Article not found")
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=f"DataBase Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Internal Server Error: {e}")

@article_router.post(
    path="/crud_article/update_article",
    tags=["CRUD ARTICLE"]
)
def update_article(
        articleId: int,
        update_data: dict
):
    try:
        article_service_obj = ArticlesService()
        article_service_obj.update_article(articleId=articleId, update_data=update_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid Input")
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail="Article not found")
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=f"DataBase Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Internal Server Error: {e}")