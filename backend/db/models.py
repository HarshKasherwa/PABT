from datetime import datetime
from enum import Enum

from sqlalchemy import Integer, String, ForeignKey, Column, ARRAY, TypeDecorator, DateTime, Sequence, Identity
from sqlalchemy.orm import declarative_base, class_mapper, relationship

Base = declarative_base()

# validate model object against SQLAlchemy model class
def validate_model_object(model_obj):
    model_class = model_obj.__class__
    for column in model_obj.__table__.columns:
        column_name = column.name
        value = getattr(model_obj, column_name)
        if value is None:
            continue  # Skip validation for attributes that are not set
        attr = getattr(model_class, column_name)
        if isinstance(attr.type, TypeDecorator):
            attr_obj = type(attr.type)
            if (
                value not in attr_obj.enum_class.__members__
                and not isinstance(value, attr_obj.enum_class)
            ):
                raise ValueError(
                    f"Invalid value for field: {column_name}"
                )
        elif isinstance(attr.type, DateTime):
            if not (
                isinstance(value, datetime)
                or (isinstance(value, str) and datetime.fromisoformat(value))
            ):
                raise ValueError(
                    f"Invalid datetime format for field: {column_name}"
                )
        else:
            # validate other key value pairs
            attr_type = attr.type.python_type
            if not isinstance(value, attr_type):
                raise ValueError(
                    f"Invalid value for field: {column_name}"
                )
    return True


# method to validate dictionary against SQLAlchemy model class
def validate_dict_against_model(model_class, data: dict):
    """
    Validate dictionary against SQLAlchemy model class.
    Check for primary key, ENUMs and datetime objects
    """
    mapper = class_mapper(model_class)
    model_obj = model_class()
    model_columns = mapper.columns.keys()
    primary_key = mapper.primary_key[0].name
    foreign_keys = [
        fk.parent.name for fk in model_class.__table__.foreign_keys
    ]
    # if not primary_key in list(data.keys()):
    #     raise db_ae.ValueError(f"Primary key {mapper.primary_key[0].name} is missing")
    for key, value in data.items():

        # Check for custom validators
        if hasattr(model_class, f"validate_{key}"):
            validator = getattr(model_class, f"validate_{key}")
            validator(model_obj, key, value)

        # Check for foreign key validators
        if key in foreign_keys:
            fk_model = [
                foreign_key.column.table.name
                for foreign_key in mapper.columns[key].foreign_keys
            ]
            if hasattr(fk_model, f"validate_{key}"):
                validator = getattr(fk_model, f"validate_{key}")
                validator(fk_model, key, value)
            else:
                # if custom validator not present
                # check for type of column type and match value accordingly
                key_type = mapper.columns[key].type.python_type
                if not isinstance(value, key_type):
                    raise ValueError(f"Invalid value for field: {key}")

        # validate rest of the key value pairs in the dict
        column_name = key
        if column_name not in model_columns:
            raise ValueError(f"Invalid field: {column_name}")
        attr = getattr(model_class, key)
        # validate ENUMs
        if isinstance(attr.type, TypeDecorator):
            attr_obj = type(attr.type)
            if (
                value not in attr_obj.enum_class.__members__
                and not isinstance(value, attr_obj.enum_class)
            ):
                raise ValueError(
                    f"Invalid value for field: {column_name}"
                )
        # validate datetime objects
        if isinstance(attr.type, DateTime):
            if not (
                isinstance(value, datetime)
                or (isinstance(value, str) and datetime.fromisoformat(value))
            ):
                raise ValueError(
                    f"Invalid datetime format for field: {column_name}"
                )
    return True


# method to convert AION models object to dictionary for JSON parsing
# includes ENUMS used in the models and datetime objects in iso format
def model_obj_to_dict(obj):
    """Convert SQLAlchemy model object to dictionary, handling datetime objects."""
    if isinstance(obj, Enum):
        # return [model_obj_to_dict(item) for item in obj]
        return obj.name
    elif isinstance(obj, ARRAY):
        return [model_obj_to_dict(item) for item in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif hasattr(obj, "__dict__"):
        return {
            key: model_obj_to_dict(value)
            for key, value in obj.__dict__.items()
            if not key.startswith("_")
        }
    else:
        return obj


# method to convert dictionary to AION models object
# Handles the ENUM types in the models and the datetime iso format to datetime object
def dict_to_model_obj(model_class, data):
    """Convert dictionary to SQLAlchemy model object, handling Enum types."""
    model_obj = model_class()
    for key, value in data.items():
        if hasattr(model_class, key):
            attr = getattr(model_class, key)
            if isinstance(attr.type, TypeDecorator):
                # create the object of the attribute type
                try:
                    attr_obj = type(attr.type)
                    enum_obj = attr_obj.enum_class
                    value = enum_obj[value]
                except Exception as e:
                    raise ValueError(str(e))
            if isinstance(attr.type, DateTime):
                value = datetime.fromisoformat(value)
            setattr(model_obj, key, value)
    return model_obj

class Users(Base):
    __tablename__ = "Users"

    """
        Users: Table Schema

        | Column Name    | Data Type | Nullable |
        |----------------|-----------|----------|
        | userId         | int       | No       |
        | username       | string    | No       |
        | password       | string    | Yes      |

    """
    userId = Column(Integer, Identity(start=101), primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=True)

    # Define the relationship to Articles
    article = relationship(
        "Articles",
        back_populates="users",
        cascade="all, delete-orphan",
    )

class Articles(Base):
    __tablename__ = "Articles"

    """
        Articles: Table Schema

        | Column Name    | Data Type | Nullable |
        |----------------|-----------|----------|
        | articleId      | int       | No       |
        | userId (FK)    | int       | No       |
        | title          | string    | No       |
        | tags           | array     | Yes      |

    """
    articleId = Column(Integer, Identity(start=101), primary_key=True)
    # ForeignKey to User.userId
    userId = Column(
        Integer,
        ForeignKey("Users.userId", ondelete="CASCADE"),
        nullable=False,
    )
    title = Column(String, nullable=False)
    tags = Column(ARRAY(String), nullable=True)

    # Define the relationship to Users
    users = relationship(
        "Users", back_populates="article"
    )