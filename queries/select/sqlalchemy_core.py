import logging

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select

logging.basicConfig(format="%(message)s", level="INFO")
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Define the database connection string
engine = create_engine('postgresql+psycopg2://workshop:workshop@localhost/workshop')
metadata = MetaData()

# Define the table reflection
users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String),
              Column('email', String),
              autoload_with=engine)


logging.info('\n\n\n\n\nStarting query:')
# Create a select query
query = select(users)

# Execute the query
with engine.connect() as connection:
    result = connection.execute(query)
    for row in result:
        logging.info(f"{row}, {type(row)}")
        # From the docs: The .Row object seeks to act as much like a Python named tuple as possible.
