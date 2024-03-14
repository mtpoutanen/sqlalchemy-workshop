import psycopg2

# Connect to your postgres DB
conn = psycopg2.connect(
    dbname="workshop",
    user="workshop",
    password="workshop",
    host="localhost",
    port="5432"
)

# Open a cursor to perform database operations
with conn.cursor() as cur:
    # Execute a query
    cur.execute("""SELECT users.id, users.name, users.email, posts.title, posts.content FROM users
                    JOIN posts ON users.id = posts.user_id""")

    # Retrieve query results
    records = cur.fetchall()
    for record in records:
        print(record, type(record))

conn.close()
