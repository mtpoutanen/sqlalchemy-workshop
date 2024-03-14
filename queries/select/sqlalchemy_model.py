from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


# Define the User model
class User(Base):
    __tablename__ = 'users'

    # Column definitions are replaced by Mapped type definitions and mapped_column function calls in our codebase
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

    def __repr__(self):
        return f"User(id={self.id}, name=\"{self.name}\", email=\"{self.email}\")"


# Define the database connection string
engine = create_engine('postgresql+psycopg2://workshop:workshop@localhost/workshop', echo=True)
Session = sessionmaker(bind=engine)

# Execute a query
with Session() as session:
    results = session.query(User).order_by(User.id)
    for result in results:
        print(repr(result), type(result))
