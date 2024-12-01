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

@crud_router.get(
    path="/crud_user/get_user",
    tags=["CRUD USER"]
)
def get_user(
        username:str
):
    try:
        user_service_obj = UsersService()
        user = user_service_obj.get_user(filters={"username": username}, single_record=True)
        return user
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail="User not found")
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
