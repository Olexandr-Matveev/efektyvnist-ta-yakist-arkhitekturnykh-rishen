from abc import ABC, abstractmethod


# ==========================================
# 1. Цільовий інтерфейс (Target)
# ==========================================
class Notification(ABC):
    """
    Загальний інтерфейс, який використовує клієнтський код.
    Змінювати його не можна (згідно з завданням).
    """

    @abstractmethod
    def send(self, title: str, message: str) -> None:
        pass


# ==========================================
# 2. Існуючий клас (Existing Class)
# ==========================================
class EmailNotification(Notification):
    """
    Стандартний клас відправки Email, який вже є в системі.
    Він прямо реалізує інтерфейс Notification.
    """

    def __init__(self, admin_email: str):
        self.admin_email = admin_email

    def send(self, title: str, message: str) -> None:
        # Імітація відправки пошти
        print(f"[Email] Відправлено на '{self.admin_email}': Заголовок='{title}', Текст='{message}'")


# ==========================================
# 3. Адаптовувані класи (Adaptees)
# Це сторонні класи або старі бібліотеки, інтерфейс яких
# несумісний з Notification. Ми не можемо їх змінювати.
# ==========================================

class SlackService:
    """
    Сторонній сервіс для роботи зі Slack.
    Має специфічні методи авторизації та відправки.
    """

    def login(self, login: str, api_key: str):
        # Логіка авторизації
        print(f"[Slack System] Авторизація користувача '{login}'...")

    def send_message_to_chat(self, chat_id: str, text: str):
        # Логіка відправки повідомлення в конкретний чат
        print(f"[Slack System] Повідомлення в чат {chat_id}: '{text}'")


class SmsService:
    """
    Сторонній сервіс для відправки SMS.
    Вимагає номер телефону та ім'я відправника.
    """

    def send_sms(self, phone: str, sender: str, text: str):
        # Логіка відправки SMS
        print(f"[SMS System] SMS від '{sender}' на номер {phone}: '{text}'")


# ==========================================
# 4. Адаптери (Adapters)
# Вони реалізують інтерфейс Notification, але всередині
# викликають методи адаптовуваних класів.
# ==========================================

class SlackAdapter(Notification):
    """
    Адаптер для Slack.
    Перетворює виклик send() у послідовність дій для SlackService.
    """

    def __init__(self, slack_service: SlackService, login: str, api_key: str, chat_id: str):
        self.slack_service = slack_service
        self.login = login
        self.api_key = api_key
        self.chat_id = chat_id

    def send(self, title: str, message: str) -> None:
        # Адаптація: авторизуємось і відправляємо повідомлення.
        # Заголовок (title) додаємо до тіла повідомлення, бо Slack приймає лише текст.
        self.slack_service.login(self.login, self.api_key)

        full_message = f"[{title}] {message}"
        self.slack_service.send_message_to_chat(self.chat_id, full_message)


class SmsAdapter(Notification):
    """
    Адаптер для SMS.
    Перетворює виклик send() у виклик send_sms().
    """

    def __init__(self, sms_service: SmsService, phone: str, sender: str):
        self.sms_service = sms_service
        self.phone = phone
        self.sender = sender

    def send(self, title: str, message: str) -> None:
        # Адаптація: SMS зазвичай короткі, об'єднуємо заголовок і текст.
        full_text = f"{title}: {message}"
        self.sms_service.send_sms(self.phone, self.sender, full_text)


# ==========================================
# 5. Клієнтський код (Client Code)
# ==========================================

def client_code(notification: Notification):
    """
    Клієнтський код працює з будь-яким об'єктом, що підтримує інтерфейс Notification.
    Йому байдуже, чи це Email, чи Slack через адаптер.
    """
    notification.send("Важлива новина", "Сервер буде перезавантажено о 23:00.")


if __name__ == "__main__":
    print("=== Тестування системи сповіщень (Патерн Адаптер) ===\n")

    # 1. Стандартна відправка Email
    print("--- 1. Email (Стандарт) ---")
    email_notifier = EmailNotification("admin@example.com")
    client_code(email_notifier)

    print("\n--- 2. Slack (Через Адаптер) ---")
    # Створюємо об'єкт стороннього сервісу
    slack_service = SlackService()
    # Огортаємо його в адаптер, передаючи необхідні дані для авторизації та чату
    slack_adapter = SlackAdapter(slack_service, "user_dev", "xoxb-12345", "#general")
    # Клієнтський код працює так само
    client_code(slack_adapter)

    print("\n--- 3. SMS (Через Адаптер) ---")
    # Створюємо об'єкт стороннього сервісу
    sms_service = SmsService()
    # Огортаємо в адаптер
    sms_adapter = SmsAdapter(sms_service, "+380501234567", "IT-Dept")
    # Клієнтський код працює так само
    client_code(sms_adapter)
