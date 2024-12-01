from typing import Optional, List

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError, NoResultFound, DatabaseError
from starlette.exceptions import HTTPException

from db.db_service_layer import UsersService, ArticlesService
from db.models import Users, Articles

crud_router = APIRouter()

@crud_router.post(
    path="/crud_user/insert_new_user",
    tags=["CRUD USER"]
)
def insert_new_user(
        username: str,
        password: str,
):
    try:
        user = Users(
            username=username,
            password=password
        )
        user_service_obj = UsersService()
        user_service_obj.insert_new_user(user=user)
        return {"message": "User created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid Input")
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="User already exists")
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=f"DataBase Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Internal Server Error: {e}")

@crud_router.get(
    path="/crud_user/get_users",
    tags=["CRUD USER"]
)
def get_users():
    try:
        user_service_obj = UsersService()
        users = user_service_obj.get_user(filters={})
        return users
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail="Users not found")
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=f"DataBase Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Internal Server Error: {e}")

@crud_router.delete(
    path="/crud_user/delete_user",
    tags=["CRUD USER"]
)
def delete_user(
        userId: int
):
    try:
        user_service_obj = UsersService()
        user_service_obj.delete_user(userId=userId)
        return {"message": f"User {userId} deleted successfully"}
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail="User not found")
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=f"DataBase Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Internal Server Error: {e}")


class ArticleCreateRequest(BaseModel):
    wikiId: int
    userId: int
    title: str
    tags: Optional[List[str]] = None

@crud_router.post(
    path="/crud_article/insert_article",
    tags=["CRUD ARTICLE"]
)
def insert_article(
        wikiId: int,
        userId: int,
        title: str,
        tags: Optional[List[str]] = None
):
    print(f"tags: {tags}")
    print(f"type: {type(tags)}")
    try:
        if tags is None or tags == []:
            article_data = Articles(
                wikiId=wikiId,
                userId=userId,
                title=title
            )
        else:
            article_data = Articles(
                wikiId=wikiId,
                userId=userId,
                title=title,
                tags=tags
            )
        article_service_obj = ArticlesService()
        article_service_obj.insert_new_article(article=article_data)
        return {"message": "Article details saved successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid Input")
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=f"DataBase Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Internal Server Error: {e}")

@crud_router.get(
    path="/crud_article/get_articles",
    tags=["CRUD ARTICLE"]
)
def get_articles(
        # userId: int
):
    try:
        article_service_obj = ArticlesService()
        # articles = article_service_obj.get_articles(filters={"userId": userId})
        articles = article_service_obj.get_articles()
        return articles
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail="Articles not found")
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=f"DataBase Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Internal Server Error: {e}")

@crud_router.get(
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

@crud_router.delete(
    path="/crud_article/delete_article",
    tags=["CRUD ARTICLE"]
)
def delete_article(
        articleId: int
):
    try:
        article_service_obj = ArticlesService()
        article_service_obj.delete_article(articleId=articleId)
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail="Article not found")
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=f"DataBase Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Internal Server Error: {e}")

@crud_router.post(
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