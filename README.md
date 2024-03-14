# SQLAlchemy and Alembic Workshop

## Goals of this workshop

At the end of this workshop, you should:
- Understand what an Object-Relational-Mapper (ORM) is and how it works
- Understand the basics of SQLAlchemy and how to interact with a database with it
- Feel comfortable writing your own SQLAlchemy models and queries using patterns in our codebase

You should also:
- Understand what migrations are and how they work
- Understand how to use Alembic to manage database migrations
- Feel comfortable writing your own migrations using the scripts in our database

## ORM Basics

ORMs provide a way to map database tables to classes and rows in those tables to instances of those classes.

### Benefits of using an ORM
- ORM abstracts away the details of the database access, transactions etc. and reduces bugs in those areas
- ORM allows you to write database-agnostic code (not a massive benefit for us, but still nice)
- Increased security, as ORMs can help prevent SQL injection attacks
- Easier to write and maintain code
- ...without an ORM library all that happens is that you'll end up writing your own, less functional ORM

## SQLAlchemy Basics

SQLAlchemy is a popular ORM for Python. It comprises two main components: the Core and the ORM. The Core is a
SQL toolkit and expression language, while the ORM is a high-level interface for interacting with databases. 
The ORM uses the Core under the hood.

In our codebase we use the ORM component of SQLAlchemy.

### Demoing the different approaches

The difference between raw sql, the core and the ORM is demonstrated in these scripts:
[raw_sql.py](queries/select/raw_sql.py)
[sqlalchemy_core.py](queries/select/sqlalchemy_core.py)
[sqlalchemy_model.py](queries/select/sqlalchemy_model.py)

If you want to try these yourself, you'll first need to start up the database:
```bash
docker compose up
```

And create the `users` table with this script (since we haven't created any migrations yet):
[create_users_table.sql](scripts/create_users_table.sql)

### Metadata object

In SQLAlchemy, the `MetaData` object serves as a container for schema and database table definitions. 
It holds a collection of Table objects as well as associated objects such as Sequence, ForeignKey, and others 
that are used to define the database schema. `MetaData` is a central catalog of all schema definitions in SQLAlchemy.

It can also be used to create and drop schemas which we actually do when we run our tests.

### Declarative Base

The `declarative_base` is a factory function that constructs a base class for database models. It serves the same
purpose as the `MetaData` object when using the Core, but is used to define models when using the ORM.

## Order Management Codebase

### Shared SQLAlchemy dependencies

#### Database engine

In our codebase we have already created many of the abstractions you need to interact with the database.
The database engine is shared as a dependency (at service level).

(Template WebAPI example)[https://github.com/PostiDigital/order-management/blob/main/packages/services/template_webapi/app/dependencies.py]

#### Transaction context

We also have a shared transaction context that you can use to interact with the database.
(Transaction Context)[https://github.com/PostiDigital/order-management/blob/main/packages/common/helpers/transaction_context.py]

### Defining models

In our codebase each microservice must define its own base model that inherits from the `Base` class 
in the `common` package.
[base.py](https://github.com/PostiDigital/order-management/blob/main/packages/common/models/database/base_db_entity.py)
Example of a service-level Base class in the `template_webapi` microservice:
[base.py](https://github.com/PostiDigital/order-management/blob/main/packages/services/template_webapi/app/models/database/base.py)

And finally, here is a simple model definition in the `template_webapi` microservice:
[demotable.py](https://github.com/PostiDigital/order-management/blob/main/packages/services/template_webapi/app/models/database/demo/demotable.py)

### Writing queries

Our codebase has 3 layers for most CRUD operations:
- Repository
- Service
- Controller

The repository layer is responsible for interacting with the database. We have a base repository class that
already contains some common methods for interacting with the database. Here is the base repository class:
[base_repository.py](https://github.com/PostiDigital/order-management/blob/main/packages/common/repositories/base_repository.py)
Note that the base repository class is generic and can be used for any model.

Here is an example of a repository class in the `template_webapi` microservice:
[demotable_repository.py](https://github.com/PostiDigital/order-management/blob/main/packages/services/template_webapi/app/repositories/demotable_repository.py)

Note that the repository calls that modify the database accept an optional "autocommit" parameter. For simple operations
this is fine, otherwise you should use the transaction context to manage the transaction.

Here is an example of a serivce class in the `template_webapi` microservice:
[demotable_repository.py](https://github.com/PostiDigital/order-management/blob/main/packages/services/template_webapi/app/services/demotable_service.py)


## ORM negatives

- Performance: ORMs can be slower than raw SQL (lazy loading, n+1 queries) if you're not careful, see example in [sqlalchemy_model.py](queries/joined_queries/sqlalchemy_model.py)
- Complexity: ORMs can be complex and difficult to understand