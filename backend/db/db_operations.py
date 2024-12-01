from sqlalchemy import ColumnElement
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, DatabaseError, NoResultFound
from sqlalchemy.orm import sessionmaker

from db.db_connector import engine


class DBOps:
    def __init__(self):
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.db = SessionLocal()

    def insert(self, data):
        """Add and commit a new record."""
        try:
            self.db.add(data)
            self.db.commit()
            self.db.refresh(data)  # To get the latest state from the DB
            return True
        except IntegrityError as e:
            self.db.rollback()
            raise IntegrityError(statement=None, params=None, orig=e)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseError(statement=None, params=None, orig=e)

    def read(
        self,
        model,
        filters: dict = None,
        order_by_column: str = None,  # if order_by is wrt a column
        order_by_criteria: ColumnElement = None,  # if order_by is wrt a query or statement
        desc: bool = False,
        single_record: bool = False,
    ):
        """Query records based on filters."""
        try:
            query = self.db.query(model)
            if filters:
                for key, value in filters.items():
                    query = query.filter(getattr(model, key) == value)
            if order_by_column:
                order_criteria = getattr(model, order_by_column)
                if desc:
                    query = query.order_by(order_criteria.desc())
                else:
                    query = query.order_by(order_criteria)
            elif order_by_criteria is not None:
                if desc:
                    query = query.order_by(order_by_criteria.desc())
                else:
                    query = query.order_by(order_by_criteria)
            result = query.first() if single_record else query.all()
            if result is None:
                raise NoResultFound
            return result
        except NoResultFound:
            raise NoResultFound
        except SQLAlchemyError as e:
            raise DatabaseError(statement=None, params=None, orig=e)

    def update(self, model, filters: dict, update_data: dict):
        """Update records based on filters."""
        try:
            records = self.db.query(model).filter_by(**filters)
            if not records.first():
                raise NoResultFound
            records.update(update_data, synchronize_session=False)
            self.db.commit()
            return True
        except IntegrityError as e:
            self.db.rollback()
            raise IntegrityError(statement=None, params=None, orig=e)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseError(statement=None, params=None, orig=e)

    def delete_record(self, model, filters: dict):
        """Delete records based on filters."""
        try:
            records = self.db.query(model).filter_by(**filters)
            if not records.first():
                raise NoResultFound
            records.delete(synchronize_session=False)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseError(statement=None, params=None, orig=e)

    def join_read(self, model1, model2, filters: dict = None):
        """Query records based on filters."""
        try:
            query = self.db.query(model1, model2)
            if filters:
                for key, value in filters.items():
                    query = query.filter(getattr(model1, key) == value)
            return query.all()
        except NoResultFound:
            raise ValueError("No records found")
        except SQLAlchemyError as e:
            raise ValueError(f"Database error: {str(e)}")