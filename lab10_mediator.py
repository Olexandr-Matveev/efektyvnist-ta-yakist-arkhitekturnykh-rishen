from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import date


# ---------------------------------------------------------
# Інтерфейс Посередника
# ---------------------------------------------------------
class Mediator(ABC):
    """
    Інтерфейс Посередника оголошує метод, який використовується компонентами
    для сповіщення про різні події.
    """

    @abstractmethod
    def notify(self, sender: object, event: str) -> None:
        pass


# ---------------------------------------------------------
# Базовий клас Компонента
# ---------------------------------------------------------
class BaseComponent:
    """
    Базовий Компонент забезпечує зберігання екземпляра посередника
    всередині об'єктів компонентів.
    """

    def __init__(self, mediator: Mediator = None) -> None:
        self._mediator = mediator
        self.is_active = True  # Стан активності компонента

    @property
    def mediator(self) -> Mediator:
        return self._mediator

    @mediator.setter
    def mediator(self, mediator: Mediator) -> None:
        self._mediator = mediator

    def set_active(self, status: bool) -> None:
        """
        Встановлює активність компонента (доступний/недоступний).
        """
        self.is_active = status
        state = "Активний" if status else "Неактивний"
        print(f"[{self.__class__.__name__}]: Статус змінено на -> {state}")


# ---------------------------------------------------------
# Конкретні Компоненти форми
# ---------------------------------------------------------

class DatePicker(BaseComponent):
    """
    Компонент вибору дати доставки.
    """

    def select_date(self, selected_date: date) -> None:
        if not self.is_active:
            print(f"[{self.__class__.__name__}]: Неможливо обрати дату, компонент неактивний.")
            return

        print(f"[{self.__class__.__name__}]: Обрано дату доставки {selected_date}.")
        # Сповіщаємо посередника про зміну дати
        self.mediator.notify(self, "date_changed")


class TimeSlots(BaseComponent):
    """
    Компонент списку доступних проміжків часу.
    """

    def update_available_slots(self) -> None:
        if not self.is_active:
            return
        # Логіка оновлення слотів (імітація)
        print(f"[{self.__class__.__name__}]: Список часових слотів оновлено відповідно до обраної дати.")


class RecipientCheckbox(BaseComponent):
    """
    Чекбокс 'Отримувач інша особа'.
    """

    def toggle(self, is_checked: bool) -> None:
        if not self.is_active:
            print(f"[{self.__class__.__name__}]: Чекбокс заблоковано.")
            return

        print(f"[{self.__class__.__name__}]: Стан змінено на {is_checked} ('Інша особа').")

        # ВИПРАВЛЕННЯ: Спочатку зберігаємо стан, потім повідомляємо!
        self.is_checked = is_checked
        self.mediator.notify(self, "recipient_checkbox_toggled")


class RecipientInput(BaseComponent):
    """
    Поля введення даних отримувача (Ім'я, Телефон).
    """

    def __init__(self, mediator: Mediator, field_name: str):
        super().__init__(mediator)
        self.field_name = field_name
        self.is_visible = False
        self.is_required = False

    def set_visibility(self, visible: bool) -> None:
        self.is_visible = visible
        state = "Відображено" if visible else "Приховано"
        print(f"[{self.__class__.__name__} - {self.field_name}]: {state}")

    def set_required(self, required: bool) -> None:
        self.is_required = required
        state = "Обов'язкове" if required else "Необов'язкове"
        print(f"[{self.__class__.__name__} - {self.field_name}]: Поле тепер {state}")


class PickupCheckbox(BaseComponent):
    """
    Чекбокс 'Самовивіз'.
    """

    def toggle(self, is_checked: bool) -> None:
        print(f"--------------------------------------------------")
        print(f"[{self.__class__.__name__}]: Обрано опцію Самовивіз: {is_checked}")
        self.is_checked = is_checked
        # Сповіщаємо посередника про зміну типу доставки
        self.mediator.notify(self, "pickup_toggled")


# ---------------------------------------------------------
# Конкретний Посередник
# ---------------------------------------------------------
class OrderFormMediator(Mediator):
    """
    Конкретний Посередник координує взаємодію між компонентами форми замовлення.
    Він знає про всі компоненти та керує їх станами.
    """

    def __init__(self,
                 date_picker: DatePicker,
                 time_slots: TimeSlots,
                 recipient_cb: RecipientCheckbox,
                 name_input: RecipientInput,
                 phone_input: RecipientInput,
                 pickup_cb: PickupCheckbox):

        self._date_picker = date_picker
        self._time_slots = time_slots
        self._recipient_cb = recipient_cb
        self._name_input = name_input
        self._phone_input = phone_input
        self._pickup_cb = pickup_cb

        # Прив'язуємо компоненти до цього посередника
        self._date_picker.mediator = self
        self._time_slots.mediator = self
        self._recipient_cb.mediator = self
        self._name_input.mediator = self
        self._phone_input.mediator = self
        self._pickup_cb.mediator = self

    def notify(self, sender: object, event: str) -> None:
        # 1. Якщо змінилася дата -> оновити часові слоти
        if event == "date_changed":
            print(f"-> [Mediator]: Реакція на зміну дати. Оновлюю час...")
            self._time_slots.update_available_slots()

        # 2. Якщо натиснуто 'Отримувач інша особа' -> показати/приховати поля та зробити їх обов'язковими
        elif event == "recipient_checkbox_toggled":
            is_checked = getattr(sender, 'is_checked', False)
            print(f"-> [Mediator]: Реакція на зміну отримувача. Налаштовую поля введення...")

            # Змінюємо видимість та обов'язковість полів
            self._name_input.set_visibility(is_checked)
            self._name_input.set_required(is_checked)

            self._phone_input.set_visibility(is_checked)
            self._phone_input.set_required(is_checked)

        # 3. Якщо обрано 'Самовивіз' -> деактивувати поля доставки
        elif event == "pickup_toggled":
            is_pickup = getattr(sender, 'is_checked', False)
            print(f"-> [Mediator]: Реакція на самовивіз. Блокую/Розблокую поля доставки...")

            # Якщо самовивіз (True), то елементи доставки стають неактивними (False)
            delivery_active = not is_pickup

            self._date_picker.set_active(delivery_active)
            self._time_slots.set_active(delivery_active)
            self._recipient_cb.set_active(delivery_active)

            # Якщо вимкнули доставку, приховуємо поля "інша особа", якщо вони були відкриті
            if is_pickup:
                self._name_input.set_visibility(False)
                self._phone_input.set_visibility(False)


# ---------------------------------------------------------
# Клієнтський код (Симуляція роботи)
# ---------------------------------------------------------
if __name__ == "__main__":
    # Створення компонентів
    date_picker = DatePicker()
    time_slots = TimeSlots()
    recipient_cb = RecipientCheckbox()
    name_input = RecipientInput(None, "Ім'я")
    phone_input = RecipientInput(None, "Телефон")
    pickup_cb = PickupCheckbox()

    # Створення посередника та прив'язка компонентів
    mediator = OrderFormMediator(
        date_picker,
        time_slots,
        recipient_cb,
        name_input,
        phone_input,
        pickup_cb
    )

    print("=== СЦЕНАРІЙ 1: Стандартне замовлення з вибором дати ===")
    date_picker.select_date(date(2025, 10, 20))

    print("\n=== СЦЕНАРІЙ 2: Замовлення для іншої особи ===")
    # Користувач натискає галочку "Інша особа"
    recipient_cb.toggle(True)

    print("\n=== СЦЕНАРІЙ 3: Користувач передумав і обрав Самовивіз ===")
    # Користувач обирає самовивіз
    pickup_cb.toggle(True)

    print("\n=== СЦЕНАРІЙ 4: Спроба змінити дату при обраному Самовивозі ===")
    # Спроба обрати дату, коли активний самовивіз (має бути заблоковано)
    date_picker.select_date(date(2025, 10, 25))
