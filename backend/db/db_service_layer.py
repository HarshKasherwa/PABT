from sqlalchemy.exc import DatabaseError, IntegrityError, NoResultFound

from db.db_operations import DBOps
from db.models import Users, validate_dict_against_model, Articles, validate_model_object, model_obj_to_dict


class UsersService:
    def __init__(self):
        self.db_obj = DBOps()

    def insert_new_user(self, user: Users):
        """Create a new user entry"""
        try:
            validate_model_object(user)
            return self.db_obj.insert(user)
        except ValueError as e:
            raise ValueError(str(e))
        except IntegrityError as e:
            raise IntegrityError
        except DatabaseError as e:
            raise DatabaseError(statement=None, params=None, orig=e)

    def get_user(self, filters: dict = None, single_record=False):
        """Fetch user based on filters"""
        try:
            user = self.db_obj.read(
                Users, filters, single_record=single_record
            )
            return user
        except NoResultFound as e:
            raise NoResultFound(str(e))
        except DatabaseError as e:
            raise DatabaseError(statement=None, params=None, orig=e)

    def update_user(self, userId: int, update_data: dict):
        """Update a user details"""
        try:
            validate_dict_against_model(model_class=Users, data=update_data)
            filters = {"userId": userId}
            return self.db_obj.update(
                model=Users, filters=filters, update_data=update_data
            )
        except ValueError as e:
            raise ValueError(str(e))
        except NoResultFound as e:
            raise NoResultFound(str(e))
        except IntegrityError as e:
            raise IntegrityError(statement=None, params=None, orig=e)
        except DatabaseError as e:
            raise DatabaseError(statement=None, params=None, orig=e)

    def delete_user(self, userId: int):
        """Delete a user"""
        filters = {"userId": userId}
        try:
            return self.db_obj.delete_record(Users, filters)
        except NoResultFound as e:
            raise NoResultFound(str(e))
        except DatabaseError as e:
            raise DatabaseError(statement=None, params=None, orig=e)

class ArticlesService:
    def __init__(self):
        self.db_obj = DBOps()

    def insert_new_article(self, article: Articles):
        """Create a new article entry"""
        try:
            validate_model_object(article)
            print(model_obj_to_dict(article))
            print(f"valid obj")
            return self.db_obj.insert(article)
        except ValueError as e:
            raise ValueError(str(e))
        except IntegrityError as e:
            raise IntegrityError(statement=None, params=None, orig=e)
        except DatabaseError as e:
            raise DatabaseError(statement=None, params=None, orig=e)

    def get_articles(self, filters: dict = None, single_record=False):
        """Fetch articles based on filters"""
        try:
            articles = self.db_obj.read(
                Articles, filters, single_record=single_record
            )
            return articles
        except NoResultFound as e:
            raise NoResultFound(str(e))
        except DatabaseError as e:
            raise DatabaseError(statement=None, params=None, orig=e)

    def update_article(self, articleId: int, update_data: dict):
        """Update a article details"""
        try:
            validate_dict_against_model(model_class=Articles, data=update_data)
            filters = {"articleId": articleId}
            return self.db_obj.update(
                model=Articles, filters=filters, update_data=update_data
            )
        except ValueError as e:
            raise ValueError(str(e))
        except NoResultFound as e:
            raise NoResultFound(str(e))
        except IntegrityError as e:
            raise IntegrityError(params=e, orig=e)
        except DatabaseError as e:
            raise DatabaseError(statement=None, params=None, orig=e)

    def delete_article(self, articleId: int):
        """Delete a saved article"""
        filters = {"articleId": articleId}
        try:
            return self.db_obj.delete_record(Articles, filters)
        except NoResultFound as e:
            raise NoResultFound(str(e))
        except DatabaseError as e:
            raise DatabaseError(statement=None, params=None, orig=e)

