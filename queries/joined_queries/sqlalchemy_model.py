from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, joinedload

import logging
# 1. Get rid of timestamp for all modules, and set other defaults
logging.basicConfig(format="%(message)s", level="INFO")
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


Base = declarative_base()


# Define the User model
class User(Base):
    __tablename__ = 'users'

    # Column definitions are replaced by Mapped type definitions and mapped_column function calls in our codebase
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    posts = relationship("Post", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id}, name=\"{self.name}\", email=\"{self.email}\")"


class Post(Base):
    __tablename__ = 'posts'

    # Column definitions are replaced by Mapped type definitions and mapped_column function calls in our codebase
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="posts")

    def __repr__(self):
        return f"Post(id={self.id}, title=\"{self.title}\", content=\"{self.content}\")"


# Define the database connection string
engine = create_engine('postgresql+psycopg2://workshop:workshop@localhost/workshop')
Session = sessionmaker(bind=engine)

# This is just here to get some the postgres initialising logs out of the way
with Session() as session:
    session.query(User).first()

with Session() as session:
    logging.info('\n--- Query without join: ---')
    user = session.query(User).order_by(User.id).first()
    logging.info('\n--- User model: ---')
    logging.info(f"{repr(user)}, {type(user)}\n")
    logging.info('--- Before accessing posts, another query happens: ---')
    logging.info('\n--- Posts: ---')
    for post in user.posts:
        logging.info(f"{repr(post)}, {type(post)}")


    logging.info('\n\n\n--- Query with join: ---')
    user = session.query(User).join(User.posts).order_by(User.id).first()
    logging.info('\n--- User model: ---')
    logging.info(f"{repr(user)}, {type(user)}\n")
    logging.info('\n--- Posts: ---')
    for post in user.posts:
        logging.info(f"{repr(post)}, {type(post)}")
