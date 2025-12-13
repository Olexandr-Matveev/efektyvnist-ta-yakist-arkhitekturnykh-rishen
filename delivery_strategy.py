from abc import ABC, abstractmethod


# --- Інтерфейс Стратегії ---

class DeliveryStrategy(ABC):
    """
    Абстрактний базовий клас (інтерфейс) для стратегій доставки.
    Всі конкретні стратегії повинні реалізовувати метод calculate_cost.
    """

    @abstractmethod
    def calculate_cost(self, order_data: dict) -> float:
        """
        Метод розрахунку вартості доставки.

        Параметри:
        order_data (dict): Словник з даними замовлення (відстань, вага тощо).

        Повертає:
        float: Вартість доставки у грошових одиницях.
        """
        pass


# --- Конкретні Стратегії ---

class PickupStrategy(DeliveryStrategy):
    """
    Стратегія самовивозу.
    """

    def calculate_cost(self, order_data: dict) -> float:
        # При самовивозі доставка безкоштовна
        return 0.0


class ExternalDeliveryStrategy(DeliveryStrategy):
    """
    Стратегія доставки зовнішньою службою (наприклад, Glovo/Uber).
    """

    def calculate_cost(self, order_data: dict) -> float:
        # Логіка розрахунку: фіксована ставка + тариф за кілометр зовнішньої служби
        distance = order_data.get('distance_km', 0)
        base_rate = 50.0  # Базова вартість подачі
        per_km_rate = 15.0

        return base_rate + (distance * per_km_rate)


class OwnDeliveryStrategy(DeliveryStrategy):
    """
    Стратегія доставки власною кур'єрською службою.
    """

    def calculate_cost(self, order_data: dict) -> float:
        # Логіка розрахунку: тариф за км, але зі знижкою для власних клієнтів
        distance = order_data.get('distance_km', 0)
        per_km_rate = 10.0  # Дешевше, ніж зовнішня служба

        # Мінімальна вартість виїзду кур'єра
        return max(30.0, distance * per_km_rate)


# --- Контекст (Клієнтський код) ---

class OrderContext:
    """
    Клас Замовлення, який використовує стратегію для розрахунку вартості.
    """

    def __init__(self):
        # Посилання на поточну стратегію (за замовчуванням - None)
        self._delivery_strategy: DeliveryStrategy = None

    def set_delivery_strategy(self, strategy: DeliveryStrategy):
        """
        Встановлення або зміна стратегії доставки під час виконання програми.
        """
        self._delivery_strategy = strategy

    def execute_calculation(self, order_details: dict) -> float:
        """
        Делегування розрахунку вартості обраній стратегії.
        """
        if not self._delivery_strategy:
            raise Exception("Стратегія доставки не обрана!")

        result = self._delivery_strategy.calculate_cost(order_details)
        print(f"Розрахунок вартості ({type(self._delivery_strategy).__name__}): {result} грн")
        return result


# --- Демонстрація роботи (Main) ---

if __name__ == "__main__":
    # Тестові дані замовлення (наприклад, відстань 5 км)
    order_data = {'distance_km': 5.0, 'weight_kg': 2.0}

    print("=== Тестування системи розрахунку доставки ===\n")

    # Створення контексту (замовлення)
    order = OrderContext()

    # 1. Вибір самовивозу
    order.set_delivery_strategy(PickupStrategy())
    order.execute_calculation(order_data)

    # 2. Вибір зовнішньої служби доставки
    order.set_delivery_strategy(ExternalDeliveryStrategy())
    order.execute_calculation(order_data)

    # 3. Вибір власної служби доставки
    order.set_delivery_strategy(OwnDeliveryStrategy())
    order.execute_calculation(order_data)
