"""
DEPENDENCY INVERSION PRINCIPLE (DIP)

High-level modules should not depend on low-level modules.
Both should depend on abstractions.
"""

# =========================================================
# ❌ DIP VIOLATED
# =========================================================

class MySQLDatabase:
    """Low-level module"""

    def save_to_sql(self, data: str):
        print(f"Saving '{data}' to MySQL database")


class MongoDBDatabase:
    """Low-level module"""

    def save_to_mongo(self, data: str):
        print(f"Saving '{data}' to MongoDB database")


class UserService:
    """
    High-level module ❌
    Directly depends on concrete DB implementations
    """

    def __init__(self):
        self.mysql_db = MySQLDatabase()      # ❌ tight coupling
        self.mongo_db = MongoDBDatabase()    # ❌ tight coupling

    def store_user_to_sql(self, user: str):
        self.mysql_db.save_to_sql(user)

    def store_user_to_mongo(self, user: str):
        self.mongo_db.save_to_mongo(user)


"""
WHY THIS IS BAD ❌
- UserService depends on concrete DB classes
- Adding a new DB (Postgres, Redis) requires modifying UserService
- Hard to test (no mocking)
- Violates Open/Closed Principle too
"""



from abc import ABC, abstractmethod

# =========================================================
# ✅ DIP FOLLOWED
# =========================================================

class Database(ABC):
    """
    Abstraction (Interface)
    High-level and low-level depend on this
    """

    @abstractmethod
    def save(self, data: str):
        pass


class MySQLDatabaseV2(Database):
    """Low-level module"""

    def save(self, data: str):
        print(f"Saving '{data}' to MySQL database")


class MongoDBDatabaseV2(Database):
    """Low-level module"""

    def save(self, data: str):
        print(f"Saving '{data}' to MongoDB database")


class UserServiceV2:
    """
    High-level module ✅
    Depends only on abstraction
    """

    def __init__(self, database: Database):
        self.database = database

    def store_user(self, user: str):
        self.database.save(user)


if __name__ == "__main__":
    mysql = MySQLDatabaseV2()
    mongo = MongoDBDatabaseV2()

    user1 = UserServiceV2(mysql)
    user1.store_user('my sql user')
    user2 = UserServiceV2(mongo)
    user2.store_user('mongo db user')



"""
WHY THIS IS GOOD ✅
- UserService depends on abstraction, not implementation
- Easy to add new databases
- Easy to test using mocks
- Fully follows DIP
"""
