import os
from datetime import timedelta, datetime
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from authlib.jose import JsonWebToken, JoseError
from pydantic import BaseModel

from app.crud import get_user
from auth.hashing import Hasher
from db.db_service_layer import UsersService
from db.models import Users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")

# router for API Endpoint
login_router = APIRouter()

# schema for Token
class Token(BaseModel):
    access_token: str
    token_type: str


# schema for Token Data
class TokenData(BaseModel):
    userid: str | None = None

def authenticate_user(
        username: str,
        password: str,
):
    user: Users = get_user(username)
    if user:
        hasher = Hasher()
        password_verify = hasher.verify_password(password, user.password)
        if password_verify:
            return user
        else:
            raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username"
        )

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    # SECRET_KEY = config['auth']['SECRET_KEY']
    # ALGORITHM = config['auth']['ALGORITHM']
    ACCESS_TOKEN_EXPIRE_DAYS = 30

    header = {"alg": ALGORITHM}
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})

    jwt = JsonWebToken([ALGORITHM])
    encoded_jwt = jwt.encode(header, to_encode, SECRET_KEY)
    return encoded_jwt


@login_router.post(
    path="/login",
    tags=["AUTH Methods"]
)
def login(
        username: str,
        password: str
):
    form_data = OAuth2PasswordRequestForm(
        username=username,
        password=password
    )
    token = login_for_access_token(form_data)
    return token

@login_router.post(
    "/login/token",
    response_model=Token,
    # include_in_schema=False,
    tags=["AUTH Methods"]
)
def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(form_data.username,
                             form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    ACCESS_TOKEN_EXPIRE_DAYS = 30
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    # create access token with type
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def validate_token(
        token: Annotated[str, Depends(oauth2_scheme)]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        SECRET_KEY = os.getenv("SECRET_KEY")
        ALGORITHM = os.getenv("ALGORITHM")
        jwt = JsonWebToken([ALGORITHM])
        payload = jwt.decode(token, SECRET_KEY)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(userid=username)
    except JoseError:
        raise credentials_exception
    user: Users = get_user(username=token_data.userid)
    if user is None:
        raise credentials_exception
    return True

@login_router.get(
    path="/get_current_user",
    tags=["AUTH Methods"]
)
def get_current_user(token: str = Depends(oauth2_scheme)):
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    jwt = JsonWebToken([ALGORITHM])
    payload = jwt.decode(token, SECRET_KEY)
    username = payload.get("sub")
    user: Users = get_user(username)
    return {"username": user.username, "userId": user.userId}


@login_router.post(
    path="/signup",
    tags=["AUTH Methods"]
)
async def signup(
        username: str,
        password: str
):
    try:
        # encrypt password
        hasher = Hasher()
        password = hasher.get_hashed_password(password)
        user = Users(username=username, password=password)
        user_service_obj = UsersService()
        user_service_obj.insert_new_user(user=user)
        return f"User: {username} signed up successfully"
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Internal Server Error: {e}")