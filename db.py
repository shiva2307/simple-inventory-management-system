from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_URL="postgresql://postgres:2307@localhost:5432/products_db"
engine=create_engine(db_URL)
session=sessionmaker(autocommit=False,autoflush=False,bind=engine)