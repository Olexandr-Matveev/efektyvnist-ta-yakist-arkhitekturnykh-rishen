from abc import ABC, abstractmethod


# -------------------------------------------------------------------------
# Лабораторна робота №3
# Тема: Патерн проектування "Будівельник" (Builder)
# Мета: Реалізація власного QueryBuilder для різних СУБД (PostgreSQL, MySQL)
# -------------------------------------------------------------------------

class QueryBuilder(ABC):
    """
    Інтерфейс Будівельника оголошує загальні кроки побудови запиту.
    Всі конкретні будівельники повинні реалізовувати цей інтерфейс.
    """

    @abstractmethod
    def select(self, table: str, columns: list) -> 'QueryBuilder':
        """Додає частину SELECT до запиту."""
        pass

    @abstractmethod
    def where(self, condition: str) -> 'QueryBuilder':
        """Додає частину WHERE до запиту."""
        pass

    @abstractmethod
    def limit(self, limit: int) -> 'QueryBuilder':
        """Додає частину LIMIT до запиту."""
        pass

    @abstractmethod
    def get_sql(self) -> str:
        """Повертає фінальний рядок SQL-запиту."""
        pass


class PostgresQueryBuilder(QueryBuilder):
    """
    Конкретний Будівельник для PostgreSQL.
    Реалізує кроки побудови запиту відповідно до синтаксису PostgreSQL.
    """

    def __init__(self):
        self._query = {}  # Використовуємо словник для зберігання частин запиту
        self._reset()

    def _reset(self):
        self._query = {
            "select": "",
            "where": "",
            "limit": ""
        }

    def select(self, table: str, columns: list) -> 'QueryBuilder':
        # Формування рядка вибірки
        cols_str = ", ".join(columns)
        self._query["select"] = f"SELECT {cols_str} FROM {table}"
        return self

    def where(self, condition: str) -> 'QueryBuilder':
        self._query["where"] = f"WHERE {condition}"
        return self

    def limit(self, limit: int) -> 'QueryBuilder':
        self._query["limit"] = f"LIMIT {limit}"
        return self

    def get_sql(self) -> str:
        # Збирання всіх частин в один рядок
        parts = [self._query["select"], self._query["where"], self._query["limit"]]
        # Фільтруємо порожні частини та з'єднуємо
        sql = " ".join(filter(None, parts)) + ";"
        self._reset()  # Скидаємо стан після отримання результату
        return sql


class MysqlQueryBuilder(QueryBuilder):
    """
    Конкретний Будівельник для MySQL.
    Може мати відмінності в синтаксисі від PostgreSQL.
    """

    def __init__(self):
        self._query = {}
        self._reset()

    def _reset(self):
        self._query = {
            "select": "",
            "where": "",
            "limit": ""
        }

    def select(self, table: str, columns: list) -> 'QueryBuilder':
        cols_str = ", ".join(columns)
        self._query["select"] = f"SELECT {cols_str} FROM {table}"
        return self

    def where(self, condition: str) -> 'QueryBuilder':
        self._query["where"] = f"WHERE {condition}"
        return self

    def limit(self, limit: int) -> 'QueryBuilder':
        self._query["limit"] = f"LIMIT {limit}"
        return self

    def get_sql(self) -> str:
        parts = [self._query["select"], self._query["where"], self._query["limit"]]
        sql = " ".join(filter(None, parts)) + ";"
        self._reset()
        return sql


# -------------------------------------------------------------------------
# Клієнтський код
# -------------------------------------------------------------------------

def client_code(builder: QueryBuilder):
    """
    Клієнтський код працює з будь-яким екземпляром будівельника через
    загальний інтерфейс QueryBuilder. Це дозволяє використовувати один і той же
    код для побудови запитів до різних баз даних.
    """
    print(f"--- Генерування запиту для {builder.__class__.__name__} ---")

    # Ланцюжок викликів (Method Chaining)
    sql_query = (builder
                 .select("users", ["id", "username", "email"])
                 .where("age > 18")
                 .limit(10)
                 .get_sql())

    print(f"Результат: {sql_query}\n")


if __name__ == "__main__":
    # 1. Використання PostgreSQL будівельника
    postgres_builder = PostgresQueryBuilder()
    client_code(postgres_builder)

    # 2. Використання MySQL будівельника
    mysql_builder = MysqlQueryBuilder()
    client_code(mysql_builder)
