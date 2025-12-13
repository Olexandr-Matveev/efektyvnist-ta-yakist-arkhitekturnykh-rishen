from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseEntityUpdater(ABC):
    """
    Абстрактний базовий клас, що визначає скелет алгоритму оновлення сутності via REST API.
    Реалізує патерн 'Шаблонний метод'.
    """

    def update_entity(self, entity_id: int, new_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Шаблонний метод, що визначає структуру алгоритму.
        Кроки виконуються у визначеному порядку.
        """
        # 1. Отримання об'єкта [cite: 19]
        entity = self.get_entity(entity_id)
        print(f"--- Початок оновлення сутності: {entity} ---")

        # 2. Валідація даних [cite: 20]
        if not self.validate_data(entity, new_data):
            # Хук на випадок помилки валідації
            self.hook_on_validation_error(entity)
            return {"status": "error", "code": 400, "message": "Validation failed"}

        # Хук перед збереженням (можливість змінити процес)
        self.hook_before_save(entity, new_data)

        # 3. Формування запиту та збереження [cite: 21]
        self.save_data(entity, new_data)

        # 4. Формування відповіді [cite: 22]
        return self.send_response(entity)

    def get_entity(self, entity_id: int) -> str:
        """Базовий метод отримання сутності (імітація)."""
        return f"Entity_{entity_id}"

    def validate_data(self, entity: str, data: Dict[str, Any]) -> bool:
        """Базова валідація. За замовчуванням повертає True."""
        print(f"[{entity}] Базова перевірка даних...")
        return True

    def save_data(self, entity: str, data: Dict[str, Any]) -> None:
        """Базове збереження даних."""
        print(f"[{entity}] Дані збережено в БД: {data}")

    def send_response(self, entity: str) -> Dict[str, Any]:
        """Базова відповідь: тільки код та статус."""
        print(f"[{entity}] Формування стандартної відповіді.")
        return {"status": "success", "code": 200}

    # --- Хуки (Hooks) ---
    def hook_before_save(self, entity: str, data: Dict[str, Any]) -> None:
        """Хук, який можна перевизначити у підкласах."""
        pass

    def hook_on_validation_error(self, entity: str) -> None:
        """Хук, що викликається при помилці валідації."""
        pass


class ProductUpdater(BaseEntityUpdater):
    """
    Клас для оновлення Товару.
    Відмінність: сповіщення адміну при помилці валідації.
    """

    def validate_data(self, entity: str, data: Dict[str, Any]) -> bool:
        # Імітуємо перевірку: якщо ціна від'ємна - помилка
        if "price" in data and data["price"] < 0:
            print(f"[{entity}] Помилка: Ціна не може бути меншою за 0.")
            return False
        return True

    def hook_on_validation_error(self, entity: str) -> None:
        # Реалізація вимоги: сповіщення адміністратору у месенджер [cite: 24, 25, 26]
        print(f"!!! АЛЕРТ: Адміністратору надіслано повідомлення про помилку валідації товару {entity} !!!")


class UserUpdater(BaseEntityUpdater):
    """
    Клас для оновлення Користувача.
    Відмінність: заборонено змінювати email.
    """

    def validate_data(self, entity: str, data: Dict[str, Any]) -> bool:
        # Реалізація вимоги: перевірка на спробу зміни email
        if "email" in data:
            print(f"[{entity}] Помилка: Зміна поля 'email' заборонена для користувачів.")
            return False
        return super().validate_data(entity, data)


class OrderUpdater(BaseEntityUpdater):
    """
    Клас для оновлення Замовлення.
    Відмінність: повертає JSON-подання сутності у відповіді.
    """

    def send_response(self, entity: str) -> Dict[str, Any]:
        # Реалізація вимоги: повертати JSON-подання сутності
        base_response = super().send_response(entity)
        base_response["body"] = {"id": 101, "items": ["item1", "item2"], "total": 500}
        print(f"[{entity}] Додано JSON-подання замовлення у відповідь.")
        return base_response


# --- Приклад використання (Client Code) ---
if __name__ == "__main__":
    print("=== 1. Оновлення ТОВАРУ (Сценарій з помилкою валідації) ===")
    product_updater = ProductUpdater()
    # Спроба встановити від'ємну ціну
    product_updater.update_entity(1, {"name": "Laptop", "price": -100})

    print("\n=== 2. Оновлення КОРИСТУВАЧА (Спроба зміни email) ===")
    user_updater = UserUpdater()
    # Спроба змінити email
    user_updater.update_entity(42, {"username": "new_nick", "email": "test@test.com"})

    print("\n=== 3. Оновлення КОРИСТУВАЧА (Успішне) ===")
    # Валідна зміна
    user_updater.update_entity(42, {"username": "valid_nick"})

    print("\n=== 4. Оновлення ЗАМОВЛЕННЯ (Розширена відповідь) ===")
    order_updater = OrderUpdater()
    response = order_updater.update_entity(101, {"status": "shipped"})
    print(f"Результат для клієнта: {response}")
